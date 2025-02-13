import pytest # type: ignore
from  generic_utils import *

class TestClass:
    number = PositiveNumber()
    string = StringValue()

@pytest.fixture
def instance():
    return TestClass()

def test_positive_number_assignment_to_integer(instance):
    instance.number = 10
    assert instance.number == 10

def test_negative_number_assignment_to_integer(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = -5

def test_zero_assignment_to_integer(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = 0

def test_non_numeric_assignment_to_integer(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = "string"

def test_string_assignment_to_string(instance):
    instance.string = 'string'
    assert instance.string == 'string'

def test_integer_assignment_to_string(instance):
    with pytest.raises(ValueError, match="string expected"):
        instance.string = 10

def test_none_assignment_to_string(instance):
     with pytest.raises(ValueError, match="string expected"):
        instance.string = None
