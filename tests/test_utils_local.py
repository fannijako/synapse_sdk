import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest  # type: ignore

sys.modules["mssparkutils"] = MagicMock()

from src.generic_utils import Utils  # noqa: E402 pylint: disable=wrong-import-position


@pytest.fixture
def utils_instance():
    return Utils()


class TestUtilsLocal:
    def test_str_representation(self, utils_instance):
        assert str(utils_instance).startswith("Utils class with methods:")

    def test_repr_representation(self, utils_instance):
        assert repr(utils_instance) == "Utils()"

    def test_get_previous_date(self, utils_instance):
        days_back = 5
        expected_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        assert utils_instance.get_previous_date(days_back=days_back) == expected_date
