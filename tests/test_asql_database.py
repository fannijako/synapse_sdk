import pytest  # type: ignore

from src.generic_utils import AsqlDatabase


@pytest.fixture
def asql():
    return AsqlDatabase(database_name='test_database_name',
                        database_schema='test_database_schema')


class TestAsqlDatabase:
    def test_missing_database_name_raises(self):
        with pytest.raises(TypeError):
            AsqlDatabase(database_name=None, database_schema='test_database_schema')

    def test_missing_database_schema_raises(self):
        with pytest.raises(TypeError):
            AsqlDatabase(database_name='test_database_name', database_schema=None)

    def test_database_name(self, asql):
        assert asql.database_name == 'test_database_name'

    def test_database_schema(self, asql):
        assert asql.database_schema == 'test_database_schema'

    def test_database_server(self, asql):
        assert asql.database_server == 'sql-tisc-we-nonprod.database.windows.net:1433'

    def test_linked_service_name(self, asql):
        assert asql.linked_service_name == 'ls_asql_tisc'

    def test_str(self, asql):
        assert str(asql).startswith('Azure SQL database linked service to the test_database_schema')

    def test_repr(self, asql):
        assert repr(asql).startswith("AsqlDatabase(database_name=")

    def test_equal_to_itself(self, asql):
        assert asql == asql  # pylint: disable=comparison-with-itself

    def test_equal_instances(self, asql):
        asql2 = AsqlDatabase(database_name='test_database_name',
                             database_schema='test_database_schema')
        assert asql == asql2

    def test_unequal_instances(self, asql):
        asql3 = AsqlDatabase(database_name='test', database_schema='test')
        assert asql != asql3
