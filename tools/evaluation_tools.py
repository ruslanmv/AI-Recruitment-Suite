"""
Evaluation Tools for AI Recruitment Suite.

This module provides tools for evaluating candidate-to-tender matches,
saving evaluation results, and retrieving evaluation history.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import json
import sqlite3
from datetime import datetime
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool


def initialize_evaluation_database() -> None:
    """
    Initialize the evaluations table in the recruitment database.

    Creates the evaluations table if it doesn't exist, with foreign key
    references to candidates and bando_di_gara tables.

    Raises:
        sqlite3.Error: If database initialization fails
    """
    with sqlite3.connect("recruitment.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
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
        """
        )
        print("✅ 'evaluations' table initialized successfully.")


# Initialize the database table when this module is loaded
initialize_evaluation_database()


@tool
def save_evaluation_result(
    candidate_id: str, bando_id: str, match_score: int, evaluation_summary: str
) -> str:
    """
    Save the result of a candidate-to-tender evaluation to the database.

    Args:
        candidate_id: The ID of the candidate being evaluated
        bando_id: The ID of the Bando di Gara used for comparison
        match_score: Numerical score (0-100) representing the candidate's fit
        evaluation_summary: Brief text summary justifying the score

    Returns:
        str: Confirmation message with the new evaluation ID

    Raises:
        sqlite3.Error: If database operation fails

    Example:
        >>> save_evaluation_result("1", "2", 88, "Excellent match with minor gaps")
        '✅ Evaluation saved successfully. Assigned Evaluation ID: 1'
    """
    if not all([candidate_id, bando_id, evaluation_summary]) or match_score is None:
        return (
            "❌ Error: Missing one or more required parameters "
            "(candidate_id, bando_id, match_score, evaluation_summary)."
        )

    try:
        with sqlite3.connect("recruitment.db") as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()

            sql_query = """
                INSERT INTO evaluations (candidate_id, bando_id, match_score, evaluation_summary, created_at)
                VALUES (?, ?, ?, ?, ?)
            """
            data_tuple = (candidate_id, bando_id, match_score, evaluation_summary, now)

            cursor.execute(sql_query, data_tuple)
            new_evaluation_id = cursor.lastrowid
            conn.commit()

        return f"✅ Evaluation saved successfully. Assigned Evaluation ID: {new_evaluation_id}"

    except sqlite3.Error as e:
        return f"❌ Database error while saving evaluation: {str(e)}"


@tool
def get_evaluation_results(
    evaluation_id: Optional[str] = None,
    candidate_id: Optional[str] = None,
    bando_id: Optional[str] = None,
) -> str:
    """
    Retrieve saved evaluation records from the database based on optional filters.

    Args:
        evaluation_id: Optional specific ID of an evaluation to retrieve
        candidate_id: Optional candidate ID to retrieve all evaluations for
        bando_id: Optional Bando di Gara ID to retrieve all evaluations for

    Returns:
        str: JSON formatted list of matching evaluation records

    Example:
        >>> get_evaluation_results(candidate_id="1")
        '[{"evaluation_id": 1, "candidate_id": "1", ...}]'
    """
    try:
        with sqlite3.connect("recruitment.db") as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
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
