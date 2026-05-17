import pytest  # type: ignore

from src.generic_utils import KeyVault


@pytest.fixture
def keyvault():
    return KeyVault()


@pytest.fixture
def keyvault2():
    return KeyVault()


class TestKeyVault:
    def test_workspace_name(self, keyvault):
        assert keyvault.workspace_name == 'syn-tisc-d-001'

    def test_linked_service_name(self, keyvault):
        assert keyvault.linked_service_name == 'kvtisc001'

    def test_equal_instances(self, keyvault, keyvault2):
        assert keyvault == keyvault2

    def test_unequal_after_mutation(self, keyvault, keyvault2):
        keyvault2.linked_service_name = 'test_change'
        assert keyvault != keyvault2

    def test_str(self, keyvault):
        assert str(keyvault) == 'Key Vault linked service kvtisc001'

    def test_repr(self, keyvault):
        assert repr(keyvault) == 'KeyVault()'

    def test_get_connection_string_or_creds_returns_str(self, keyvault):
        assert isinstance(keyvault.get_connection_string_or_creds(), str)

    def test_get_secret_returns_str(self, keyvault):
        assert isinstance(keyvault.get_secret('ls-rest-jira-secret'), str)

    def test_put_then_get_secret_roundtrip(self, keyvault):
        keyvault.put_secret('utils-test-secret', 'test')
        assert ' '.join(keyvault.get_secret('utils-test-secret')) == 't e s t'
