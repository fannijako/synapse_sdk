from generic_utils import SynStorageAccount


synstorage = SynStorageAccount()

ERROR_MESSAGE = 'SynStorageAccount does not have the attributes of Notebook'
assert synstorage.workspace_name == 'syn-tisc-d-001', ERROR_MESSAGE

ERROR_MESSAGE = 'Linked service name is not set correctly'
assert synstorage.linked_service_name == 'dlssyntisc001', ERROR_MESSAGE

synstorage2 = SynStorageAccount()
assert synstorage == synstorage2, 'SynStorageAccounts should equal'

synstorage2.linked_service_name = 'test_change'
assert synstorage != synstorage2, 'SynStorageAccounts should not equal'
assert str(synstorage) == 'Synapse default ADLSGen2 linked service dlssyntisc001'
assert repr(synstorage) == 'SynStorageAccount()'
