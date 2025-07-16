import sqlite3
import json
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_comparison_data(candidate_id: str, bando_id: str) -> str:
    """
    NEW TOOL: Retrieves full details for a specific candidate AND a specific Bando di Gara to facilitate comparison.
    
    :param candidate_id: The ID of the candidate to retrieve.
    :param bando_id: The ID of the Bando di Gara to retrieve.
    :return: A single JSON object with two keys: 'candidate' and 'bando_di_gara'.
    """
    with sqlite3.connect('recruitment.db') as conn:
        cursor = conn.cursor()

        # Helper to convert a database row to a dictionary, parsing JSON fields
        def _row_to_dict(row, description, json_keys):
            if not row:
                return {}
            rec = dict(zip([col[0] for col in description], row))
            for key in json_keys:
                if key in rec and isinstance(rec[key], str):
                    try:
                        rec[key] = json.loads(rec[key])
                    except json.JSONDecodeError:
                        pass # Keep as string if it's not valid JSON
            return rec

        # 1. Fetch Candidate Data
        cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        candidate_row = cursor.fetchone()
        candidate_desc = cursor.description
        candidate_json_keys = ("technical_skills", "certifications", "previous_companies", 
                               "key_achievements", "languages", "industry_experience")
        candidate_data = _row_to_dict(candidate_row, candidate_desc, candidate_json_keys)

        # 2. Fetch Bando di Gara Data
        cursor.execute("SELECT * FROM bando_di_gara WHERE id = ?", (bando_id,))
        bando_row = cursor.fetchone()
        bando_desc = cursor.description
        bando_json_keys = ("required_skills", "certifications_required", "key_deliverables")
        bando_data = _row_to_dict(bando_row, bando_desc, bando_json_keys)

    # 3. Combine into a single JSON object
    comparison_payload = {
        "candidate": candidate_data,
        "bando_di_gara": bando_data
    }
    
    return json.dumps(comparison_payload, ensure_ascii=False, indent=2)


# --- Existing Tools (for context) ---

@tool
def get_info_candidate(candidate_id: str = None) -> str:
    """
    Retrieve candidate(s) from the database.
    If candidate_id is provided, returns only that candidate; otherwise returns all.
    Output is a JSON-encoded list or single object.
    """
    with sqlite3.connect('recruitment.db') as conn:
        cursor = conn.cursor()
        if candidate_id:
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        else:
            cursor.execute("SELECT * FROM candidates ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]

    def _row_to_dict(row):
        rec = dict(zip(cols, row))
        for key in ("technical_skills", "certifications", "previous_companies", 
                    "key_achievements", "languages", "industry_experience"):
            if key in rec and isinstance(rec[key], str):
                try:
                    rec[key] = json.loads(rec[key])
                except json.JSONDecodeError:
                    pass # Keep as string if it's not valid JSON
        return rec

    results = [_row_to_dict(r) for r in rows]
    if candidate_id:
        return json.dumps(results[0] if results else {}, ensure_ascii=False, indent=2)
    return json.dumps(results, ensure_ascii=False, indent=2)



@tool
def get_info_bando(bando_id: str = None) -> str:
    """
    Retrieve Bando di Gara project(s) from the database.
    If bando_id is provided, returns only that project; otherwise returns all.
    Output is a JSON-encoded list or single object.
    """
    with sqlite3.connect('recruitment.db') as conn:
        cursor = conn.cursor()
        if bando_id:
            cursor.execute("SELECT * FROM bando_di_gara WHERE id = ?", (bando_id,))
        else:
            cursor.execute("SELECT * FROM bando_di_gara ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]

    def _row_to_dict(row):
        rec = dict(zip(cols, row))
        for key in ("required_skills", "certifications_required", "key_deliverables"):
            if key in rec and isinstance(rec[key], str):
                try:
                    rec[key] = json.loads(rec[key])
                except json.JSONDecodeError:
                    pass # Keep as string if it's not valid JSON
        return rec

    results = [_row_to_dict(r) for r in rows]
    if bando_id:
        return json.dumps(results[0] if results else {}, ensure_ascii=False, indent=2)
    return json.dumps(results, ensure_ascii=False, indent=2)



    """
    Retrieve a summary list of all Bando di Gara projects (id and project_title).
    """
    with sqlite3.connect('recruitment.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_title FROM bando_di_gara ORDER BY created_at DESC")
        rows = cursor.fetchall()
    summary = [{"id": r[0], "project_title": r[1]} for r in rows]
    return json.dumps(summary, ensure_ascii=False, indent=2)