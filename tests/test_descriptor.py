import sys

from unittest.mock import MagicMock

import pytest  # type: ignore

sys.modules["mssparkutils"] = MagicMock()

from src.generic_utils import (  # noqa: E402 pylint: disable=wrong-import-position
    PositiveNumber,
    StringOrNoneValue,
    StringValue,
)


class _Target:  # pylint: disable=too-few-public-methods
    number = PositiveNumber()
    string = StringValue()
    string_or_none = StringOrNoneValue()


@pytest.fixture
def instance():
    return _Target()


class TestPositiveNumber:
    def test_positive_integer_assignment(self, instance):
        instance.number = 10
        assert instance.number == 10

    def test_positive_float_assignment(self, instance):
        instance.number = 10.2
        assert instance.number == 10.2

    def test_negative_number_raises(self, instance):
        with pytest.raises(TypeError, match="positive number expected"):
            instance.number = -5

    def test_zero_assignment(self, instance):
        instance.number = 0
        assert instance.number == 0

    def test_non_numeric_raises(self, instance):
        with pytest.raises(TypeError, match="positive number expected"):
            instance.number = "string"


class TestStringValue:
    def test_string_assignment(self, instance):
        instance.string = 'string'
        assert instance.string == 'string'

    def test_integer_raises(self, instance):
        with pytest.raises(TypeError, match="string expected"):
            instance.string = 10

    def test_none_raises(self, instance):
        with pytest.raises(TypeError, match="string expected"):
            instance.string = None


class TestStringOrNoneValue:
    def test_string_assignment(self, instance):
        instance.string_or_none = 'string'
        assert instance.string_or_none == 'string'

    def test_integer_raises(self, instance):
        with pytest.raises(TypeError, match="string expected"):
            instance.string_or_none = 10

    def test_none_assignment(self, instance):
        instance.string_or_none = None
        assert instance.string_or_none is None
