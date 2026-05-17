import pytest  # type: ignore

from src.generic_utils import SynStorageAccount


@pytest.fixture
def synstorage():
    return SynStorageAccount()


@pytest.fixture
def synstorage2():
    return SynStorageAccount()


class TestSynStorage:
    def test_workspace_name(self, synstorage):
        assert synstorage.workspace_name == 'syn-tisc-d-001'

    def test_linked_service_name(self, synstorage):
        assert synstorage.linked_service_name == 'dlssyntisc001'

    def test_equal_instances(self, synstorage, synstorage2):
        assert synstorage == synstorage2

    def test_unequal_after_mutation(self, synstorage, synstorage2):
        synstorage2.linked_service_name = 'test_change'
        assert synstorage != synstorage2

    def test_str(self, synstorage):
        assert str(synstorage) == 'Synapse default ADLSGen2 linked service dlssyntisc001'

    def test_repr(self, synstorage):
        assert repr(synstorage) == 'SynStorageAccount()'
