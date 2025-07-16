import sqlite3
import json
from datetime import datetime
from ibm_watsonx_orchestrate.agent_builder.tools import tool

# --- Step 1: Update Database Initialization ---
# This function ensures the 'evaluations' table exists.

def initialize_evaluation_database():
    """
    Connects to the database and creates the 'evaluations' table if it doesn't exist.
    This table will store the results of candidate-to-bando comparisons.
    """
    with sqlite3.connect('recruitment.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                bando_id TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                evaluation_summary TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (candidate_id) REFERENCES candidates (id),
                FOREIGN KEY (bando_id) REFERENCES bando_di_gara (id)
            )
        ''')
        print("✅ 'evaluations' table initialized successfully.")

# Initialize the database table when this module is loaded
initialize_evaluation_database()


# --- Step 2: Create the Tool to Save Evaluations ---

@tool
def save_evaluation_result(candidate_id: str, bando_id: str, match_score: int, evaluation_summary: str) -> str:
    """
    Saves the result of a candidate-to-bando evaluation to the database.

    :param candidate_id: The ID of the candidate being evaluated.
    :param bando_id: The ID of the Bando di Gara used for the comparison.
    :param match_score: A numerical score (e.g., 0-100) representing the candidate's fit.
    :param evaluation_summary: A brief text summary justifying the score.
    :return: A confirmation message with the new evaluation ID.
    """
    if not all([candidate_id, bando_id, evaluation_summary]) or match_score is None:
        return "❌ Error: Missing one or more required parameters (candidate_id, bando_id, match_score, evaluation_summary)."

    try:
        with sqlite3.connect('recruitment.db') as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            sql_query = '''
                INSERT INTO evaluations (candidate_id, bando_id, match_score, evaluation_summary, created_at)
                VALUES (?, ?, ?, ?, ?)
            '''
            data_tuple = (candidate_id, bando_id, match_score, evaluation_summary, now)
            
            cursor.execute(sql_query, data_tuple)
            new_evaluation_id = cursor.lastrowid
            conn.commit()

        return f"✅ Evaluation saved successfully. Assigned Evaluation ID: {new_evaluation_id}"

    except sqlite3.Error as e:
        return f"❌ Database error while saving evaluation: {str(e)}"


# --- Step 3: Create the NEW Tool to Retrieve Evaluations ---

@tool
def get_evaluation_results(evaluation_id: str = None, candidate_id: str = None, bando_id: str = None) -> str:
    """
    Retrieves saved evaluation records from the database based on optional filters.

    :param evaluation_id: The specific ID of an evaluation to retrieve.
    :param candidate_id: The ID of a candidate to retrieve all evaluations for.
    :param bando_id: The ID of a Bando di Gara to retrieve all evaluations for.
    :return: A JSON formatted list of matching evaluation records.
    """
    try:
        with sqlite3.connect('recruitment.db') as conn:
            conn.row_factory = sqlite3.Row # This allows accessing columns by name
            cursor = conn.cursor()
            
            query = "SELECT * FROM evaluations"
            filters = []
            params = []

            if evaluation_id:
                filters.append("evaluation_id = ?")
                params.append(evaluation_id)
            if candidate_id:
                filters.append("candidate_id = ?")
                params.append(candidate_id)
            if bando_id:
                filters.append("bando_id = ?")
                params.append(bando_id)

            if filters:
                query += " WHERE " + " AND ".join(filters)
            
            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Convert rows to a list of dictionaries
            results = [dict(row) for row in rows]
            
            if not results:
                return "No matching evaluations found."

            return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        return f"❌ Database error while retrieving evaluations: {str(e)}"