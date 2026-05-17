import pytest  # type: ignore

from src.generic_utils import Kusto


@pytest.fixture
def kusto():
    return Kusto()


@pytest.fixture
def kusto2():
    return Kusto()


class TestKusto:
    def test_workspace_name(self, kusto):
        assert kusto.workspace_name == 'syn-tisc-d-001'

    def test_linked_service_name(self, kusto):
        assert kusto.linked_service_name == 'dectisc001'

    def test_equal_instances(self, kusto, kusto2):
        assert kusto == kusto2

    def test_unequal_after_mutation(self, kusto, kusto2):
        kusto2.linked_service_name = 'test_change'
        assert kusto != kusto2

    def test_str(self, kusto):
        assert str(kusto) == 'Azure Data Explorer (Kusto) linked service dectisc001'

    def test_repr(self, kusto):
        assert repr(kusto) == 'Kusto()'

    def test_get_connection_string_or_creds_returns_str(self, kusto):
        assert isinstance(kusto.get_connection_string_or_creds(), str)
