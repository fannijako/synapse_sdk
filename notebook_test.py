import pytest  # type: ignore
import sys
from unittest.mock import MagicMock, patch

sys.modules["mssparkutils"] = MagicMock()

from generic_utils import Notebook

@pytest.fixture
def mock_mssparkutils():
    mock = MagicMock()
    mock.env.getWorkspaceName.return_value = "ws-dataproduct-env-version"
    mock.runtime.context.get.side_effect = lambda x: {
        'currentNotebookName': 'test_notebook',
        'pipelinejobid': 'pipeline123'
    }[x]
    mock.env.getJobId.return_value = "job123"
    mock.env.getPoolName.return_value = "pool123"
    mock.env.getClusterId.return_value = "cluster123"
    return mock

@patch('generic_utils.mssparkutils', new_callable=MagicMock)
def test_notebook_initialization(mock_mssparkutils, mock_mssparkutils_fixture):
    mock_mssparkutils.configure_mock(**vars(mock_mssparkutils_fixture))

    notebook = Notebook()

    assert notebook._workspace_name == "ws-dataproduct-env-version"
    assert notebook._data_product_name == "dataproduct"
    assert notebook._environment == "env"
    assert notebook._data_product_version == "version"
    assert notebook._notebook_name == "test_notebook"
    assert notebook._job_id == "job123"
    assert notebook._pipeline_job_id == "pipeline123"
    assert notebook._pool == "pool123"
    assert notebook._cluster == "cluster123"

@pytest.mark.parametrize("workspace_name, expected", [
    ("ws-product1-dev-v1", ("product1", "dev", "v1")),
    ("ws-product2-prod-v2", ("product2", "prod", "v2")),
])
@patch('generic_utils.mssparkutils', new_callable=MagicMock)
def test_workspace_name_parsing(mock_mssparkutils, workspace_name, expected):
    mock_mssparkutils.env.getWorkspaceName.return_value = workspace_name
    
    notebook = Notebook()
    
    assert notebook._data_product_name == expected[0]
    assert notebook._environment == expected[1]
    assert notebook._data_product_version == expected[2]

def test_exit_values_initialization():
    notebook = Notebook()
    assert notebook.exit_values == {}
