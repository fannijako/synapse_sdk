import builtins
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

mssparkutils_mock = MagicMock()
mssparkutils_mock.env.getWorkspaceName.return_value = "syn-tisc-d-001"
mssparkutils_mock.env.getJobId.return_value = "test-job-id"
mssparkutils_mock.env.getPoolName.return_value = "synsptisc-test-pool"
mssparkutils_mock.env.getClusterId.return_value = "test-cluster"
mssparkutils_mock.runtime.context = {
    "currentNotebookName": "test_notebook",
    "pipelinejobid": "test-pipeline-job-id",
}
mssparkutils_mock.credentials.getConnectionStringOrCreds.return_value = "test-connection-string"
secret_store = {"ls-rest-jira-secret": "test-secret"}


def _get_secret(_key_vault_name, secret_name, _linked_service_name):
    return secret_store.get(secret_name, "test-secret")


def _put_secret(_key_vault_name, secret_name, secret_value, _linked_service_name):
    secret_store[secret_name] = secret_value


mssparkutils_mock.credentials.getSecret.side_effect = _get_secret
mssparkutils_mock.credentials.putSecret.side_effect = _put_secret


def _file_info(path, size):
    return SimpleNamespace(path=path, name=path.rstrip("/").split("/")[-1], size=size)


def _ls(path):
    curated = "abfss://curated@dlstiscd001.dfs.core.windows.net"
    test_folder = f"{curated}/test"
    if path == curated:
        return [_file_info(test_folder, 0)]
    if path == test_folder:
        return [_file_info(f"{test_folder}/test.json", 1)]
    return []


mssparkutils_mock.fs.ls.side_effect = _ls

sys.modules.setdefault("mssparkutils", mssparkutils_mock)

spark_mock = MagicMock()
spark_conf = {}


def _get_conf(key):
    return spark_conf.get(key, "test_notebook_test-run-id")


def _set_conf(key, value):
    spark_conf[key] = value


spark_mock.conf.get.side_effect = _get_conf
spark_mock.conf.set.side_effect = _set_conf
builtins.spark = spark_mock
