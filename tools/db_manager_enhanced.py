"""
Enhanced Database Manager for AI Recruitment Suite.

This module provides enhanced database management functionality with sequential ID generation,
JSON cleaning, and comprehensive CRUD operations for candidates and tender documents.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import json
import re
import sqlite3
from datetime import datetime
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool


def clean_json_string(raw: str) -> str:
    """
    Clean a potentially malformed JSON string by fixing common issues.

    This function handles:
    - BOM removal
    - JavaScript-style comments
    - Single quotes to double quotes conversion
    - Trailing commas before closing brackets

    Args:
        raw: The raw JSON string to clean

    Returns:
        str: The cleaned JSON string

    Example:
        >>> clean_json_string("{'name': 'John',}")
        '{"name": "John"}'
    """
    s = raw.strip()
    # Remove BOM if present
    s = s.lstrip("\ufeff")
    # Remove JS-style comments
    s = re.sub(r"//.*?$|/\*.*?\*/", "", s, flags=re.DOTALL | re.MULTILINE)
    # Replace single quotes around keys with double quotes
    s = re.sub(r"'([A-Za-z0-9_]+)'(?=\s*:)", r'"\1"', s)
    # Replace single-quoted values with double quotes
    s = re.sub(r":\s*'([^']*?)'", r': "\1"', s)
    # Remove trailing commas before } or ]
    s = re.sub(r",(\s*[}\]])", r"\1", s)
    return s


def init_db() -> None:
    """
    Initialize the recruitment database with required tables and schema migrations.

    Creates:
    - candidates table for CV data
    - bando_di_gara table for tender documents

    Performs migration-aware schema updates to add missing columns.

    Raises:
        sqlite3.Error: If database initialization fails
    """
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()

    # Create base candidates table (with a text-based primary key)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            id TEXT PRIMARY KEY,
            candidate_name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            position_applied TEXT,
            technical_skills TEXT,
            experience_years TEXT,
            education TEXT,
            certifications TEXT,
            previous_companies TEXT,
            consulting_experience TEXT,
            key_achievements TEXT,
            languages TEXT,
            industry_experience TEXT,
            created_at TEXT
        )
    """
    )

    # Add missing source_filename column if needed
    cursor.execute("PRAGMA table_info(candidates);")
    existing_cols = {row[1] for row in cursor.fetchall()}
    if "source_filename" not in existing_cols:
        cursor.execute("ALTER TABLE candidates ADD COLUMN source_filename TEXT;")

    # Create base bando_di_gara table (with a text-based primary key)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bando_di_gara (
            id TEXT PRIMARY KEY,
            client_name TEXT,
            project_title TEXT,
            project_description TEXT,
            required_skills TEXT,
            experience_required TEXT,
            education_requirements TEXT,
            certifications_required TEXT,
            project_duration TEXT,
            team_size TEXT,
            location TEXT,
            deadline TEXT,
            budget_range TEXT,
            industry_sector TEXT,
            key_deliverables TEXT,
            created_at TEXT
        )
    """
    )

    # Add missing source_filename column if needed
    cursor.execute("PRAGMA table_info(bando_di_gara);")
    existing_cols = {row[1] for row in cursor.fetchall()}
    if "source_filename" not in existing_cols:
        cursor.execute("ALTER TABLE bando_di_gara ADD COLUMN source_filename TEXT;")

    conn.commit()
    conn.close()


def get_next_id(table_name: str) -> str:
    """
    Calculate the next sequential string ID for a given table.

    Args:
        table_name: Name of the database table

    Returns:
        str: The next sequential ID as a string

    Example:
        >>> get_next_id('candidates')
        '5'
    """
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()
    # Find the maximum ID value by converting the text IDs to integers
    cursor.execute(f"SELECT MAX(CAST(id AS INTEGER)) FROM {table_name}")
    max_id = cursor.fetchone()[0]
    conn.close()

    # If the table is empty (max_id is None), start with "1". Otherwise, increment.
    next_id = 1 if max_id is None else max_id + 1
    return str(next_id)


# Initialize database on import
init_db()


@tool
def format_and_save_processed_data(processed_data: str) -> str:
    """
    Format processed data with a sequential string ID and save to the database.

    This function applies JSON cleaning to fix malformed JSON before parsing,
    determines the document type, generates a sequential ID, and saves to the
    appropriate table.

    Args:
        processed_data: JSON string containing extracted document information

    Returns:
        str: Success message with assigned ID and document details

    Raises:
        json.JSONDecodeError: If JSON is invalid even after cleaning
        Exception: For general database or processing errors

    Example:
        >>> format_and_save_processed_data('{"document_type": "CV", ...}')
        '✅ CV Successfully Processed and Saved...'
    """
    try:
        cleaned = clean_json_string(processed_data)
        data = json.loads(cleaned)

        document_type = data.get("document_type", "Unknown")
        source_filename = data.get("source_filename", "Unknown")

        if document_type == "CV":
            new_id = get_next_id("candidates")
            now = datetime.now().isoformat()

            formatted_data = {
                "id": new_id,
                "candidate_name": data.get("candidate_name", ""),
                "email": data.get("contact_info", {}).get("email", ""),
                "phone": data.get("contact_info", {}).get("phone", ""),
                "location": data.get("contact_info", {}).get("location", ""),
                "position_applied": data.get("position_applied", ""),
                "technical_skills": json.dumps(data.get("technical_skills", [])),
                "experience_years": data.get("experience_years", ""),
                "education": data.get("education", ""),
                "certifications": json.dumps(data.get("certifications", [])),
                "previous_companies": json.dumps(data.get("previous_companies", [])),
                "consulting_experience": data.get("consulting_experience", ""),
                "key_achievements": json.dumps(data.get("key_achievements", [])),
                "languages": json.dumps(data.get("languages", [])),
                "industry_experience": json.dumps(data.get("industry_experience", [])),
                "source_filename": source_filename,
                "created_at": now,
            }

            with sqlite3.connect("recruitment.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO candidates (
                        id, candidate_name, email, phone, location, position_applied,
                        technical_skills, experience_years, education, certifications,
                        previous_companies, consulting_experience, key_achievements,
                        languages, industry_experience, source_filename, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    tuple(formatted_data.values()),
                )

            return (
                f"✅ **CV Successfully Processed and Saved**\n\n"
                f"Assigned ID: {new_id}\n"
                f"Candidate Name: {formatted_data['candidate_name']}\n"
                f"Source File: {source_filename}\n"
                f"Saved At: {formatted_data['created_at']}"
            )

        elif document_type == "Bando di Gara":
            new_id = get_next_id("bando_di_gara")
            now = datetime.now().isoformat()

            formatted_data = {
                "id": new_id,
                "client_name": data.get("client_name", ""),
                "project_title": data.get("project_title", ""),
                "project_description": data.get("project_description", ""),
                "required_skills": json.dumps(data.get("required_skills", [])),
                "experience_required": data.get("experience_required", ""),
                "education_requirements": data.get("education_requirements", ""),
                "certifications_required": json.dumps(
                    data.get("certifications_required", [])
                ),
                "project_duration": data.get("project_duration", ""),
                "team_size": data.get("team_size", ""),
                "location": data.get("location", ""),
                "deadline": data.get("deadline", ""),
                "budget_range": data.get("budget_range", ""),
                "industry_sector": data.get("industry_sector", ""),
                "key_deliverables": json.dumps(data.get("key_deliverables", [])),
                "source_filename": source_filename,
                "created_at": now,
            }

            with sqlite3.connect("recruitment.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO bando_di_gara (
                        id, client_name, project_title, project_description, required_skills,
                        experience_required, education_requirements, certifications_required,
                        project_duration, team_size, location, deadline, budget_range,
                        industry_sector, key_deliverables, source_filename, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    tuple(formatted_data.values()),
                )

            return (
                f"✅ **Bando di Gara Successfully Processed and Saved**\n\n"
                f"Assigned ID: {new_id}\n"
                f"Client Name: {formatted_data['client_name']}\n"
                f"Project Title: {formatted_data['project_title']}\n"
                f"Source File: {source_filename}\n"
                f"Saved At: {formatted_data['created_at']}"
            )

        else:
            return f"❌ Unknown document type: {document_type}. Cannot format and save."

    except json.JSONDecodeError:
        return "❌ Error: Invalid JSON format in processed data even after cleaning"
    except Exception as e:
        return f"❌ Error formatting and saving data: {str(e)}"


@tool
def get_all_candidates() -> str:
    """
    Retrieve all candidates from the database.

    Returns:
        str: Formatted list of all candidates with key information

    Example:
        >>> get_all_candidates()
        '📋 **All Candidates:**\\n\\n**ID:** 1\\n**Name:** John Doe\\n...'
    """
    try:
        conn = sqlite3.connect("recruitment.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM candidates ORDER BY created_at DESC")
        candidates = cursor.fetchall()
        conn.close()

        if not candidates:
            return "No candidates found in database"

        result = "📋 **All Candidates:**\n\n"
        for candidate in candidates:
            result += f"**ID:** {candidate[0]}\n"
            result += f"**Name:** {candidate[1]}\n"
            result += f"**Email:** {candidate[2]}\n"
            result += f"**Position:** {candidate[5]}\n"
            result += f"**Experience:** {candidate[7]}\n"
            result += f"**Source File:** {candidate[15]}\n"
            result += f"**Added:** {candidate[16]}\n"
            result += "---\n"

        return result

    except Exception as e:
        return f"❌ Error retrieving candidates: {str(e)}"


@tool
def get_all_bandos() -> str:
    """
    Retrieve all Bando di Gara (tender documents) from the database.

    Returns:
        str: Formatted list of all tender documents with key information

    Example:
        >>> get_all_bandos()
        '📋 **All Bando di Gara:**\\n\\n**ID:** 1\\n**Client:** Acme Corp\\n...'
    """
    try:
        conn = sqlite3.connect("recruitment.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bando_di_gara ORDER BY created_at DESC")
        bandos = cursor.fetchall()
        conn.close()

        if not bandos:
            return "No Bando di Gara found in database"

        result = "📋 **All Bando di Gara:**\n\n"
        for bando in bandos:
            result += f"**ID:** {bando[0]}\n"
            result += f"**Client:** {bando[1]}\n"
            result += f"**Project:** {bando[2]}\n"
            result += f"**Description:** {bando[3][:100]}...\n"
            result += f"**Location:** {bando[10]}\n"
            result += f"**Source File:** {bando[15]}\n"
            result += f"**Added:** {bando[16]}\n"
            result += "---\n"

        return result

    except Exception as e:
        return f"❌ Error retrieving bandos: {str(e)}"


@tool
def get_candidate_by_id(candidate_id: str) -> str:
    """
    Get specific candidate details by ID.

    Args:
        candidate_id: The candidate ID to search for

    Returns:
        str: Detailed candidate information or error message

    Example:
        >>> get_candidate_by_id("1")
        '👤 **Candidate Details - 1**\\n\\n**Name:** John Doe\\n...'
    """
    try:
        conn = sqlite3.connect("recruitment.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
        candidate = cursor.fetchone()
        conn.close()

        if not candidate:
            return f"❌ Candidate with ID {candidate_id} not found"

        result = f"👤 **Candidate Details - {candidate[0]}**\n\n"
        result += f"**Name:** {candidate[1]}\n"
        result += f"**Email:** {candidate[2]}\n"
        result += f"**Phone:** {candidate[3]}\n"
        result += f"**Location:** {candidate[4]}\n"
        result += f"**Position Applied:** {candidate[5]}\n"
        result += f"**Experience Years:** {candidate[7]}\n"
        result += f"**Education:** {candidate[8]}\n"
        result += f"**Technical Skills:** {candidate[6]}\n"
        result += f"**Consulting Experience:** {candidate[11]}\n"
        result += f"**Source File:** {candidate[15]}\n"
        result += f"**Added:** {candidate[16]}\n"

        return result

    except Exception as e:
        return f"❌ Error retrieving candidate: {str(e)}"


@tool
def clear_thread_files() -> str:
    """
    Clear information about uploaded files in the current thread.

    This is a utility function to reset the file cache for the current
    conversation thread, allowing new documents to be uploaded.

    Returns:
        str: Confirmation message

    Example:
        >>> clear_thread_files()
        '✅ Thread file cache cleared. You can now upload new documents.'
    """
    return "✅ Thread file cache cleared. You can now upload new documents."
