import pytest
from  generic_utils import *

class TestClass:
    number = PositiveNumber()

@pytest.fixture
def instance():
    return TestClass()

def test_positive_number_assignment(instance):
    instance.number = 10
    assert instance.number == 10

def test_negative_number_assignment(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = -5

def test_zero_assignment(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = 0

def test_non_numeric_assignment(instance):
    with pytest.raises(ValueError, match="positive number expected"):
        instance.number = "string"
