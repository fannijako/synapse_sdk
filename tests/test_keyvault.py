from generic_utils import KeyVault


keyvault = KeyVault()

ERROR_MESSAGE = 'Keyvault does not have the attributes of Notebook'
assert keyvault.workspace_name == 'syn-tisc-d-001', ERROR_MESSAGE

ERROR_MESSAGE =  'Linked service name is not set correctly'
assert keyvault.linked_service_name == 'kvtisc001', ERROR_MESSAGE

keyvault2 = KeyVault()
assert keyvault == keyvault2, 'KeyVaults should equal'

keyvault2.linked_service_name = 'test_change'
assert keyvault != keyvault2, 'KeyVaults should not equal'
assert str(keyvault) == 'Key Vault linked service kvtisc001'
assert repr(keyvault) == 'KeyVault()'

ERROR_MESSAGE = 'get_connection_string_or_creds not defined correctly'
assert isinstance(keyvault.get_connection_string_or_creds(), str), ERROR_MESSAGE

ERROR_MESSAGE =  'get_secret not defined correctly'
assert isinstance(keyvault.get_secret('ls-rest-jira-secret'), str), ERROR_MESSAGE

keyvault.put_secret('utils-test-secret', 'test')
ERROR_MESSAGE = 'put_secret not defined correctly'
assert ' '.join(keyvault.get_secret('utils-test-secret')) == 't e s t', ERROR_MESSAGE
