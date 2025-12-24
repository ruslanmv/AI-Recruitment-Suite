"""
Database Retrieval Tools for AI Recruitment Suite.

This module provides tools for retrieving candidate and tender information
from the recruitment database, including comparison data for evaluations.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import json
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from ibm_watsonx_orchestrate.agent_builder.tools import tool


def _row_to_dict(
    row: Optional[Tuple], description: List[Tuple], json_keys: Tuple[str, ...]
) -> Dict[str, Any]:
    """
    Convert a database row to a dictionary, parsing JSON fields.

    Args:
        row: Database row tuple
        description: Cursor description with column information
        json_keys: Tuple of column names that contain JSON data

    Returns:
        Dict[str, Any]: Dictionary representation of the row
    """
    if not row:
        return {}

    rec = dict(zip([col[0] for col in description], row))
    for key in json_keys:
        if key in rec and isinstance(rec[key], str):
            try:
                rec[key] = json.loads(rec[key])
            except json.JSONDecodeError:
                pass  # Keep as string if it's not valid JSON
    return rec


@tool
def get_comparison_data(candidate_id: str, bando_id: str) -> str:
    """
    Retrieve full details for a candidate and tender document for comparison.

    This tool fetches both candidate and tender information in a single call,
    making it ideal for evaluation and matching operations.

    Args:
        candidate_id: The ID of the candidate to retrieve
        bando_id: The ID of the Bando di Gara to retrieve

    Returns:
        str: JSON object with 'candidate' and 'bando_di_gara' keys

    Example:
        >>> get_comparison_data("1", "2")
        '{"candidate": {...}, "bando_di_gara": {...}}'
    """
    with sqlite3.connect("recruitment.db") as conn:
        cursor = conn.cursor()

        # Fetch Candidate Data
        cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        candidate_row = cursor.fetchone()
        candidate_desc = cursor.description
        candidate_json_keys = (
            "technical_skills",
            "certifications",
            "previous_companies",
            "key_achievements",
            "languages",
            "industry_experience",
        )
        candidate_data = _row_to_dict(candidate_row, candidate_desc, candidate_json_keys)

        # Fetch Bando di Gara Data
        cursor.execute("SELECT * FROM bando_di_gara WHERE id = ?", (bando_id,))
        bando_row = cursor.fetchone()
        bando_desc = cursor.description
        bando_json_keys = (
            "required_skills",
            "certifications_required",
            "key_deliverables",
        )
        bando_data = _row_to_dict(bando_row, bando_desc, bando_json_keys)

    # Combine into a single JSON object
    comparison_payload = {"candidate": candidate_data, "bando_di_gara": bando_data}

    return json.dumps(comparison_payload, ensure_ascii=False, indent=2)


@tool
def get_info_candidate(candidate_id: Optional[str] = None) -> str:
    """
    Retrieve candidate(s) from the database.

    Args:
        candidate_id: Optional candidate ID. If provided, returns only that candidate;
                     otherwise returns all candidates

    Returns:
        str: JSON-encoded candidate data (single object or list)

    Example:
        >>> get_info_candidate("1")
        '{"id": "1", "candidate_name": "John Doe", ...}'
    """
    with sqlite3.connect("recruitment.db") as conn:
        cursor = conn.cursor()
        if candidate_id:
            cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        else:
            cursor.execute("SELECT * FROM candidates ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]

    def row_to_dict(row: Tuple) -> Dict[str, Any]:
        rec = dict(zip(cols, row))
        for key in (
            "technical_skills",
            "certifications",
            "previous_companies",
            "key_achievements",
            "languages",
            "industry_experience",
        ):
            if key in rec and isinstance(rec[key], str):
                try:
                    rec[key] = json.loads(rec[key])
                except json.JSONDecodeError:
                    pass
        return rec

    results = [row_to_dict(r) for r in rows]
    if candidate_id:
        return json.dumps(results[0] if results else {}, ensure_ascii=False, indent=2)
    return json.dumps(results, ensure_ascii=False, indent=2)


@tool
def get_info_bando(bando_id: Optional[str] = None) -> str:
    """
    Retrieve Bando di Gara project(s) from the database.

    Args:
        bando_id: Optional tender ID. If provided, returns only that project;
                 otherwise returns all projects

    Returns:
        str: JSON-encoded tender data (single object or list)

    Example:
        >>> get_info_bando("2")
        '{"id": "2", "client_name": "Acme Corp", ...}'
    """
    with sqlite3.connect("recruitment.db") as conn:
        cursor = conn.cursor()
        if bando_id:
            cursor.execute("SELECT * FROM bando_di_gara WHERE id = ?", (bando_id,))
        else:
            cursor.execute("SELECT * FROM bando_di_gara ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]

    def row_to_dict(row: Tuple) -> Dict[str, Any]:
        rec = dict(zip(cols, row))
        for key in (
            "required_skills",
            "certifications_required",
            "key_deliverables",
        ):
            if key in rec and isinstance(rec[key], str):
                try:
                    rec[key] = json.loads(rec[key])
                except json.JSONDecodeError:
                    pass
        return rec

    results = [row_to_dict(r) for r in rows]
    if bando_id:
        return json.dumps(results[0] if results else {}, ensure_ascii=False, indent=2)
    return json.dumps(results, ensure_ascii=False, indent=2)
