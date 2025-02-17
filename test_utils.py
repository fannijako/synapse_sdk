import pytest # type: ignore
import sys

from unittest.mock import MagicMock
from datetime import datetime, timedelta

sys.modules["mssparkutils"] = MagicMock()

from  generic_utils import Utils


@pytest.fixture
def utils_instance():
    return Utils()

def test_str_representation(utils_instance):
    assert str(utils_instance).startswith("Utils class with methods:"), "Incorrect __str__ representation"

def test_repr_representation(utils_instance):
    assert repr(utils_instance) == "Utils()", "Incorrect __repr__ representation"

def test_get_previous_date(utils_instance):
    days_back = 5
    expected_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    assert utils_instance.get_previous_date(days_back = days_back) == expected_date, "get_previous_date did not return the correct date"
