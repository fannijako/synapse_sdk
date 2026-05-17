import pytest  # type: ignore

from src.generic_utils import AzureMachineLearningWorkspace


@pytest.fixture
def azureml():
    return AzureMachineLearningWorkspace()


@pytest.fixture
def azureml2():
    return AzureMachineLearningWorkspace()


class TestAzureML:
    def test_workspace_name(self, azureml):
        assert azureml.workspace_name == 'syn-tisc-d-001'

    def test_linked_service_name(self, azureml):
        assert azureml.linked_service_name == 'mlwtisc001'

    def test_equal_instances(self, azureml, azureml2):
        assert azureml == azureml2

    def test_unequal_after_mutation(self, azureml, azureml2):
        azureml2.linked_service_name = 'test_change'
        assert azureml != azureml2

    def test_str(self, azureml):
        assert str(azureml) == 'Azure Machine Learning linked service mlwtisc001'

    def test_repr(self, azureml):
        assert repr(azureml) == 'AzureMachineLearningWorkspace()'

    def test_get_connection_string_or_creds_returns_str(self, azureml):
        assert isinstance(azureml.get_connection_string_or_creds(), str)
