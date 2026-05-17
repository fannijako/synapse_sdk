import builtins  # noqa: C0413
from datetime import datetime, timedelta

import pytest  # type: ignore

from src.generic_utils import Notebook

spark = getattr(builtins, 'spark', None)  # pylint: disable=invalid-name


@pytest.fixture
def notebook():
    return Notebook()


@pytest.fixture
def notebook2():
    return Notebook()


@pytest.fixture(autouse=True)
def _reset_exit_values():
    Notebook.exit_values = {}
    yield
    Notebook.exit_values = {}


class TestNotebookClassState:
    def test_exit_values_is_dict_on_class(self):
        assert isinstance(Notebook.exit_values, dict)

    def test_exit_values_initially_empty_on_class(self):
        assert len(Notebook.exit_values.keys()) == 0

    def test_exit_values_is_dict_on_instance(self, notebook):
        assert isinstance(notebook.exit_values, dict)

    def test_exit_values_initially_empty_on_instance(self, notebook):
        assert len(notebook.exit_values.keys()) == 0


class TestNotebookDefaults:
    def test_get_previous_date(self, notebook):
        expected = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        assert notebook.get_previous_date(5) == expected

    def test_workspace_name(self, notebook):
        assert notebook.workspace_name == 'syn-tisc-d-001'

    def test_data_product_name(self, notebook):
        assert notebook.data_product_name == 'tisc'

    def test_environment(self, notebook):
        assert notebook.environment == 'd'

    def test_data_product_version(self, notebook):
        assert notebook.data_product_version == "001"

    def test_azure_storage_name(self, notebook):
        assert notebook.azure_storage_name == 'dlstiscd001'

    def test_curated_path(self, notebook):
        assert notebook.curated_path == 'abfss://curated@dlstiscd001.dfs.core.windows.net'

    def test_standardized_curated_path(self, notebook):
        expected = 'abfss://curated@dlstiscd001.dfs.core.windows.net/standardized'
        assert notebook.standardized_curated_path == expected

    def test_sensitive_standardized_curated_path(self, notebook):
        expected = 'abfss://curated@dlstiscd001.dfs.core.windows.net/sensitive-standardized'
        assert notebook.sensitive_standardized_curated_path == expected

    def test_trusted_path(self, notebook):
        assert notebook.trusted_path == 'abfss://trusted@dlstiscd001.dfs.core.windows.net'

    def test_notebook_name(self, notebook):
        assert notebook.notebook_name == 'test_notebook'

    def test_job_id_is_str(self, notebook):
        assert isinstance(notebook.job_id, str)

    def test_pipeline_job_id_is_str(self, notebook):
        assert isinstance(notebook.pipeline_job_id, str)

    def test_pool_prefix(self, notebook):
        assert notebook.pool.startswith('synsptisc')

    def test_cluster_is_str(self, notebook):
        assert isinstance(notebook.cluster, str)


class TestNotebookSparkConfRebase:
    def test_datetime_rebase_read(self):
        assert spark.conf.get("spark.sql.legacy.parquet.datetimeRebaseModeInRead") == "CORRECTED"  # type: ignore

    def test_datetime_rebase_write(self):
        assert spark.conf.get("spark.sql.legacy.parquet.datetimeRebaseModeInWrite") == "CORRECTED"  # type: ignore

    def test_int96_rebase_read(self):
        assert spark.conf.get("spark.sql.legacy.parquet.int96RebaseModeInRead") == "CORRECTED"  # type: ignore

    def test_int96_rebase_write(self):
        assert spark.conf.get("spark.sql.legacy.parquet.int96RebaseModeInWrite") == "CORRECTED"  # type: ignore


class TestNotebookReprAndEquality:
    def test_self_equality(self, notebook):
        assert notebook == notebook  # pylint: disable=comparison-with-itself

    def test_str(self, notebook):
        assert str(notebook).startswith('test_notebook in syn-tisc-d-001 executed by ')

    def test_repr(self, notebook):
        assert repr(notebook) == "Notebook()"

    def test_two_instances_equal(self, notebook, notebook2):
        assert notebook == notebook2


class TestNotebookReadonlyAttributes:
    def test_workspace_name_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.workspace_name = 'test'

    def test_workspace_name_unchanged_after_failed_write(self, notebook):
        with pytest.raises(AttributeError):
            notebook.workspace_name = 'test'
        assert notebook.workspace_name == 'syn-tisc-d-001'

    def test_notebook_name_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.notebook_name = 'test_new'

    def test_notebook_name_unchanged_after_failed_write(self, notebook):
        with pytest.raises(AttributeError):
            notebook.notebook_name = 'test_new'
        assert notebook.notebook_name == 'test_notebook'

    def test_job_id_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.job_id = 'test_new'

    def test_pipeline_job_id_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.pipeline_job_id = 'test_new'

    def test_pool_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.pool = 'test_new'

    def test_cluster_is_readonly(self, notebook):
        with pytest.raises(AttributeError):
            notebook.cluster = 'test_new'


class TestNotebookValidatedSetters:
    def test_data_product_name_rejects_non_string(self, notebook):
        with pytest.raises(TypeError):
            notebook.data_product_name = 10

    def test_environment_rejects_non_string(self, notebook):
        with pytest.raises(ValueError):
            notebook.environment = 10

    def test_environment_rejects_unknown_value(self, notebook):
        with pytest.raises(ValueError):
            notebook.environment = "s"

    def test_environment_unchanged_after_invalid(self, notebook):
        with pytest.raises(ValueError):
            notebook.environment = 10
        assert notebook.environment == 'd'

    def test_azure_storage_name_setter_warns(self, notebook):
        with pytest.raises(UserWarning):
            notebook.azure_storage_name = "test"

    def test_azure_storage_name_unchanged_after_warning(self, notebook):
        with pytest.raises(UserWarning):
            notebook.azure_storage_name = "test"
        assert notebook.azure_storage_name == "dlstiscd001"

    def test_curated_path_setter_warns(self, notebook):
        with pytest.raises(UserWarning):
            notebook.curated_path = 'test'

    def test_curated_path_unchanged_after_warning(self, notebook):
        with pytest.raises(UserWarning):
            notebook.curated_path = 'test'
        assert notebook.curated_path == 'abfss://curated@dlstiscd001.dfs.core.windows.net'

    def test_standardized_curated_path_setter_warns(self, notebook):
        with pytest.raises(UserWarning):
            notebook.standardized_curated_path = 'test'

    def test_standardized_curated_path_unchanged_after_warning(self, notebook):
        with pytest.raises(UserWarning):
            notebook.standardized_curated_path = 'test'
        expected = 'abfss://curated@dlstiscd001.dfs.core.windows.net/standardized'
        assert notebook.standardized_curated_path == expected

    def test_sensitive_standardized_curated_path_setter_warns(self, notebook):
        with pytest.raises(UserWarning):
            notebook.sensitive_standardized_curated_path = 'test'

    def test_sensitive_standardized_curated_path_unchanged_after_warning(self, notebook):
        with pytest.raises(UserWarning):
            notebook.sensitive_standardized_curated_path = 'test'
        expected = 'abfss://curated@dlstiscd001.dfs.core.windows.net/sensitive-standardized'
        assert notebook.sensitive_standardized_curated_path == expected

    def test_trusted_path_setter_warns(self, notebook):
        with pytest.raises(UserWarning):
            notebook.trusted_path = 'test'

    def test_trusted_path_unchanged_after_warning(self, notebook):
        with pytest.raises(UserWarning):
            notebook.trusted_path = 'test'
        assert notebook.trusted_path == 'abfss://trusted@dlstiscd001.dfs.core.windows.net'


class TestNotebookDerivedPathsAfterMutation:
    @pytest.fixture
    def mutated_notebook(self, notebook):
        notebook.data_product_name = 'coca'
        notebook.environment = 'p'
        notebook.data_product_version = '002'
        return notebook

    def test_data_product_name_updated(self, mutated_notebook):
        assert mutated_notebook.data_product_name == 'coca'

    def test_environment_updated(self, mutated_notebook):
        assert mutated_notebook.environment == 'p'

    def test_data_product_version_updated(self, mutated_notebook):
        assert mutated_notebook.data_product_version == '002'

    def test_azure_storage_name_recomputed(self, mutated_notebook):
        assert mutated_notebook.azure_storage_name == 'dlscocap002'

    def test_curated_path_recomputed(self, mutated_notebook):
        assert mutated_notebook.curated_path == 'abfss://curated@dlscocap002.dfs.core.windows.net'

    def test_standardized_curated_path_recomputed(self, mutated_notebook):
        expected = 'abfss://curated@dlscocap002.dfs.core.windows.net/standardized'
        assert mutated_notebook.standardized_curated_path == expected

    def test_sensitive_standardized_curated_path_recomputed(self, mutated_notebook):
        expected = 'abfss://curated@dlscocap002.dfs.core.windows.net/sensitive-standardized'
        assert mutated_notebook.sensitive_standardized_curated_path == expected

    def test_trusted_path_recomputed(self, mutated_notebook):
        assert mutated_notebook.trusted_path == 'abfss://trusted@dlscocap002.dfs.core.windows.net'


class TestNotebookSetExitValue:
    def test_set_string_value(self, notebook):
        notebook.set_exit_value(key='test_str_key', value='test1')
        assert notebook.exit_values.get('test_str_key') == 'test1'

    def test_set_string_value_visible_on_class(self, notebook):
        notebook.set_exit_value(key='test_str_key', value='test1')
        assert Notebook.exit_values.get('test_str_key') == 'test1'

    def test_set_int_value_raises(self, notebook):
        with pytest.raises(TypeError):
            notebook.set_exit_value(key='test_error_value', value=10)

    def test_failed_set_does_not_mutate_existing(self, notebook):
        notebook.set_exit_value(key='test_str_key', value='test1')
        with pytest.raises(TypeError):
            notebook.set_exit_value(key='test_error_value', value=10)
        assert notebook.exit_values.get('test_str_key') == 'test1'

    def test_overwrite_string_value(self, notebook):
        notebook.set_exit_value(key='test_str_key', value='test1')
        notebook.set_exit_value(key='test_str_key', value='test2')
        assert notebook.exit_values.get('test_str_key') == 'test2'

    def test_set_list_value(self, notebook):
        notebook.set_exit_value(key='test_list_key', value=['test3'])
        assert notebook.exit_values.get('test_list_key') == ['test3']

    def test_list_value_extends_with_list(self, notebook):
        notebook.set_exit_value(key='test_list_key', value=['test3'])
        notebook.set_exit_value(key='test_list_key', value=['test4'])
        assert notebook.exit_values.get('test_list_key') == ['test3', 'test4']

    def test_list_value_extends_with_string(self, notebook):
        notebook.set_exit_value(key='test_list_key', value=['test3'])
        notebook.set_exit_value(key='test_list_key', value=['test4'])
        notebook.set_exit_value(key='test_list_key', value='test5')
        assert notebook.exit_values.get('test_list_key') == ['test3', 'test4', 'test5']

    def test_state_shared_across_instances(self, notebook, notebook2):
        notebook.set_exit_value(key='test_list_key', value=['test3', 'test4', 'test5'])
        notebook2.set_exit_value(key='test_list_key', value='test6')
        expected = ['test3', 'test4', 'test5', 'test6']
        assert notebook.exit_values.get('test_list_key') == expected
        assert notebook2.exit_values.get('test_list_key') == expected
        assert Notebook.exit_values.get('test_list_key') == expected


class TestNotebookExit:
    def test_exit(self, notebook):
        notebook.exit()
