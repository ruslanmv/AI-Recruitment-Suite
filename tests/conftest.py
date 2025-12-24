"""
Pytest configuration and fixtures.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import pytest


@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration."""
    return {"database": "recruitment.db", "test_mode": True}
