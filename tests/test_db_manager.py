"""
Unit tests for database manager module.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import json
import sqlite3
from datetime import datetime

import pytest

from tools.db_manager_enhanced import (
    clean_json_string,
    get_next_id,
    init_db,
)


@pytest.fixture
def test_db():
    """Create a test database."""
    init_db()
    yield
    # Cleanup after tests
    try:
        conn = sqlite3.connect("recruitment.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates")
        cursor.execute("DELETE FROM bando_di_gara")
        conn.commit()
        conn.close()
    except Exception:
        pass


@pytest.mark.unit
def test_clean_json_string():
    """Test JSON string cleaning functionality."""
    malformed = "{'name': 'John', 'age': 30,}"
    cleaned = clean_json_string(malformed)
    assert json.loads(cleaned) == {"name": "John", "age": 30}


@pytest.mark.unit
def test_get_next_id(test_db):
    """Test sequential ID generation."""
    next_id = get_next_id("candidates")
    assert next_id == "1"


@pytest.mark.unit
def test_init_db():
    """Test database initialization."""
    init_db()
    conn = sqlite3.connect("recruitment.db")
    cursor = conn.cursor()

    # Check if candidates table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='candidates'")
    assert cursor.fetchone() is not None

    # Check if bando_di_gara table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='bando_di_gara'"
    )
    assert cursor.fetchone() is not None

    conn.close()
