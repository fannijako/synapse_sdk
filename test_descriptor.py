import pytest # type: ignore
import sys
from unittest.mock import MagicMock, patch

sys.modules["mssparkutils"] = MagicMock()

from  generic_utils import PositiveNumber, StringValue

class TestClass:
    number = PositiveNumber()
    string = StringValue()

@pytest.fixture
def instance():
    return TestClass()

def test_positive_number_assignment_to_positive_number(instance):
    instance.number = 10
    assert instance.number == 10, "Positive integer can't be assigned to PositiveNumber."

def test_float_assignment_to_positive_number(instance):
    instance.number = 10.2
    assert instance.number == 10.2, "Positive float can't be assigned to PositiveNumber."

def test_negative_number_assignment_to_positive_number(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = -5

def test_zero_assignment_to_positive_number(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = 0

def test_non_numeric_assignment_to_positive_number(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = "string"

def test_string_assignment_to_string(instance):
    instance.string = 'string'
    assert instance.string == 'string', "String can't be assigned to StringValue."

def test_integer_assignment_to_string(instance):
    with pytest.raises(ValueError, match="string expected"):
        instance.string = 10

def test_none_assignment_to_string(instance):
     with pytest.raises(ValueError, match="string expected"):
        instance.string = None
