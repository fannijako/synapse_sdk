from generic_utils import Kusto


kusto = Kusto()

ERROR_MESSAGE = 'Kusto does not have the attributes of Notebook'
assert kusto.workspace_name == 'syn-tisc-d-001', ERROR_MESSAGE

ERROR_MESSAGE = 'Linked service name is not set correctly'
assert kusto.linked_service_name == 'dectisc001', ERROR_MESSAGE

kusto2 = Kusto()
assert kusto == kusto2, 'Kustos should equal'

kusto2.linked_service_name = 'test_change'
assert kusto != kusto2, 'Kustos should not equal'
assert str(kusto) == 'Azure Data Explorer (Kusto) linked service dectisc001'
assert repr(kusto) == 'Kusto()'

ERROR_MESSAGE = 'get_connection_string_or_creds not defined correctly'
assert isinstance(kusto.get_connection_string_or_creds(), str), ERROR_MESSAGE
