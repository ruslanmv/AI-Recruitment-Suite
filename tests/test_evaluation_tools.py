"""
Unit tests for evaluation tools module.

Author: Ruslan Magana Vsevolodovna
Website: ruslanmv.com
License: Apache 2.0
"""

import pytest

from tools.evaluation_tools import initialize_evaluation_database


@pytest.mark.unit
def test_initialize_evaluation_database():
    """Test evaluation database initialization."""
    # Should not raise any exceptions
    initialize_evaluation_database()
