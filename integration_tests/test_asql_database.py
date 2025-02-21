from ..synapse_notebooks.generic_utils import AsqlDatabase


asql = AsqlDatabase(database_name = 'test_database_name', database_schema = 'test_database_schema')

try:
    asql = AsqlDatabase(database_name = None, database_schema = 'test_database_schema')
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

try:
    asql = AsqlDatabase(database_name = 'test_database_name', database_schema = None)
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

assert asql.database_name == 'test_database_name', 'Database name is not set correctly'
assert asql.database_schema == 'test_database_schema', 'Database schema is not set correctly'

ERROR_MESSAGE = 'Database server is not set correctly'
assert asql.database_server == 'sql-tisc-we-nonprod.database.windows.net:1433', ERROR_MESSAGE
assert asql.linked_service_name == 'ls_asql_tisc', 'Linked service name is not set correctly'

assert str(asql).startswith('Azure SQL database linked service to the test_database_schema')

ERROR_MESSAGE = "repr representation is not set correctly"
assert repr(asql).startswith("AsqlDatabase(database_name="), ERROR_MESSAGE

assert asql == asql, 'Instance should equal itself' # pylint: disable=comparison-with-itself

asql2 = AsqlDatabase(database_name = 'test_database_name', database_schema = 'test_database_schema')
assert asql == asql2, 'Instances should equal'
asql3 = AsqlDatabase(database_name = 'test', database_schema = 'test')
assert asql != asql3
