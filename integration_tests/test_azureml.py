from ..synapse_notebooks.generic_utils import AzureMachineLearningWorkspace


azureml = AzureMachineLearningWorkspace()

ERROR_MESSAGE = 'AzureMachineLearningWorkspace does not have the attributes of Notebook'
assert azureml.workspace_name == 'syn-tisc-d-001', ERROR_MESSAGE

ERROR_MESSAGE = 'Linked service name is not set correctly'
assert azureml.linked_service_name == 'mlwtisc001', ERROR_MESSAGE

azureml2 = AzureMachineLearningWorkspace()
assert azureml == azureml2, 'AzureMachineLearningWorkspaces should equal'

azureml2.linked_service_name = 'test_change'
assert azureml != azureml2, 'AzureMachineLearningWorkspaces should not equal'
assert str(azureml) == 'Azure Machine Learning linked service mlwtisc001'
assert repr(azureml) == 'AzureMachineLearningWorkspace()'

ERROR_MESSAGE = 'get_connection_string_or_creds not defined correctly'
assert isinstance(azureml.get_connection_string_or_creds(), str), ERROR_MESSAGE
