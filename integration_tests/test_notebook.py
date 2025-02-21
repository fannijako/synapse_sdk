from generic_utils import Notebook # pylint: disable=wrong-import-order

from datetime import datetime, timedelta

notebook = Notebook()

assert isinstance(Notebook.exit_values, dict)
assert len(Notebook.exit_values.keys()) == 0

assert isinstance(notebook.exit_values, dict)
assert len(notebook.exit_values.keys()) == 0

expected = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
assert notebook.get_previous_date(5) == expected, "Get previous date is not defined properly"

assert notebook.workspace_name == 'syn-tisc-d-001', "Workspace_name is not set correctly"

assert notebook.data_product_name == 'tisc', "Data product name is not set correctly"
assert notebook.environment == 'd', "Environment was not set correctly"
assert notebook.data_product_version == "001", "Data product version is not set correctly"

ERROR_MESSAGE = "Azure storage name was not changed accordingly"
assert notebook.azure_storage_name == 'dlstiscd001', ERROR_MESSAGE

ERROR_MESSAGE = "Path was not changed accordingly"
assert notebook.curated_path == 'abfss://curated@dlstiscd001.dfs.core.windows.net', ERROR_MESSAGE

EXPECTED = 'abfss://curated@dlstiscd001.dfs.core.windows.net/standardized'
assert notebook.standardized_curated_path == expected, ERROR_MESSAGE

EXPECTED = 'abfss://curated@dlstiscd001.dfs.core.windows.net/sensitive-standardized'
assert notebook.sensitive_standardized_curated_path == expected, ERROR_MESSAGE
assert notebook.trusted_path == 'abfss://trusted@dlstiscd001.dfs.core.windows.net', ERROR_MESSAGE

assert notebook.notebook_name == 'test_notebook', "Notebook name was not set correctly"
assert isinstance(notebook.job_id, str)
assert isinstance(notebook.pipeline_job_id, str)
assert notebook.pool.startswith('synsptisc'), "Pool was not initiated correctly"
assert isinstance(notebook.cluster, str)

assert spark.conf.get("spark.sql.legacy.parquet.datetimeRebaseModeInRead") == "CORRECTED" # type: ignore # pylint: disable=undefined-variable
assert spark.conf.get("spark.sql.legacy.parquet.datetimeRebaseModeInWrite") == "CORRECTED" # type: ignore # pylint: disable=undefined-variable
assert spark.conf.get("spark.sql.legacy.parquet.int96RebaseModeInRead") == "CORRECTED" # type: ignore # pylint: disable=undefined-variable
assert spark.conf.get("spark.sql.legacy.parquet.int96RebaseModeInWrite") == "CORRECTED" # type: ignore # pylint: disable=undefined-variable

assert notebook == notebook, "Notebook does not equal itself" # pylint: disable=comparison-with-itself

ERROR_MESSAGE = "str not defined properly"
assert str(notebook).startswith('test_notebook in syn-tisc-d-001 executed by '), ERROR_MESSAGE
assert repr(notebook) == "Notebook()", "Representation is not set properly"

try:
    notebook.workspace_name = 'test'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

assert notebook.workspace_name == 'syn-tisc-d-001', "Workspace_name is not set correctly"

try:
    notebook.data_product_name = 10
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

try:
    notebook.environment = 10
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

assert notebook.environment == 'd', "Environment has been changed"

try:
    notebook.environment = "s"
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

assert notebook.environment == 'd', "Environment has been changed"

try:
    notebook.azure_storage_name = "test"
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

assert notebook.azure_storage_name == "dlstiscd001", "azure_storage_name has been changed"

try:
    notebook.curated_path = 'test'
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

EXPECTED = 'abfss://curated@dlstiscd001.dfs.core.windows.net'
assert notebook.curated_path == EXPECTED, "curated_path has been changed"

try:
    notebook.standardized_curated_path = 'test'
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

EXPECTED = 'abfss://curated@dlstiscd001.dfs.core.windows.net/standardized'
ERROR_MESSAGE = "standardized_curated_path has been changed"
assert notebook.standardized_curated_path == EXPECTED, ERROR_MESSAGE

try:
    notebook.sensitive_standardized_curated_path = 'test'
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

EXPECTED = 'abfss://curated@dlstiscd001.dfs.core.windows.net/sensitive-standardized'
ERROR_MESSAGE = "sensitive_standardized_curated_path has been changed"
assert notebook.sensitive_standardized_curated_path == EXPECTED, ERROR_MESSAGE

try:
    notebook.trusted_path = 'test'
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

EXPECTED = 'abfss://trusted@dlstiscd001.dfs.core.windows.net'
ERROR_MESSAGE = "trusted_path has been changed"
assert notebook.trusted_path == EXPECTED, ERROR_MESSAGE

try:
    notebook.notebook_name = 'test_new'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

assert notebook.notebook_name == 'test_notebook', "notebook_name has been changed"

try:
    notebook.job_id = 'test_new'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

try:
    notebook.pipeline_job_id = 'test_new'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

try:
    notebook.pool = 'test_new'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

try:
    notebook.cluster = 'test_new'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

notebook.data_product_name = 'coca'
notebook.environment = 'p'
notebook.data_product_version = '002'

assert notebook.data_product_name == 'coca', "Data product name was not changed"
assert notebook.environment == 'p', "Environment was not changed"
assert notebook.data_product_version == '002', "Data product name was not changed"

ERROR_MESSAGE = 'Attribute was not changed accordingly'
assert notebook.azure_storage_name == 'dlscocap002', ERROR_MESSAGE
assert notebook.curated_path == 'abfss://curated@dlscocap002.dfs.core.windows.net', ERROR_MESSAGE

EXPECTED = 'abfss://curated@dlscocap002.dfs.core.windows.net/standardized'
assert notebook.standardized_curated_path == EXPECTED, ERROR_MESSAGE

EXPECTED = 'abfss://curated@dlscocap002.dfs.core.windows.net/sensitive-standardized'
assert notebook.sensitive_standardized_curated_path == EXPECTED, ERROR_MESSAGE
assert notebook.trusted_path == 'abfss://trusted@dlscocap002.dfs.core.windows.net', ERROR_MESSAGE

notebook.set_exit_value(key = 'test_str_key', value = 'test1')

assert notebook.exit_values.get('test_str_key') == 'test1', 'Exit value not set correctly'
assert Notebook.exit_values.get('test_str_key') == 'test1', 'Exit value not set correctly'

try:
    notebook.set_exit_value(key = 'test_error_value', value = 10)
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

ERROR_MESSAGE = 'Exit value not set correctly'
assert notebook.exit_values.get('test_str_key') == 'test1', ERROR_MESSAGE
assert Notebook.exit_values.get('test_str_key') == 'test1', ERROR_MESSAGE

notebook.set_exit_value(key = 'test_str_key', value = 'test2')

assert notebook.exit_values.get('test_str_key') == 'test2', ERROR_MESSAGE
assert Notebook.exit_values.get('test_str_key') == 'test2', ERROR_MESSAGE

notebook.set_exit_value(key = 'test_list_key', value = ['test3'])

assert notebook.exit_values.get('test_list_key') == ['test3'], ERROR_MESSAGE
assert Notebook.exit_values.get('test_list_key') == ['test3'], ERROR_MESSAGE

notebook.set_exit_value(key = 'test_list_key', value = ['test4'])

assert notebook.exit_values.get('test_list_key') == ['test3', 'test4'],ERROR_MESSAGE
assert Notebook.exit_values.get('test_list_key') == ['test3', 'test4'], ERROR_MESSAGE

notebook.set_exit_value(key = 'test_list_key', value = 'test5')

assert notebook.exit_values.get('test_list_key') == ['test3', 'test4', 'test5'], ERROR_MESSAGE
assert Notebook.exit_values.get('test_list_key') == ['test3', 'test4', 'test5'], ERROR_MESSAGE

notebook2 = Notebook()

assert notebook == notebook2, "Notebooks should equal"
notebook2.set_exit_value(key = 'test_list_key', value = 'test6')

EXPECTED = ['test3', 'test4', 'test5', 'test6']
assert notebook.exit_values.get('test_list_key') == EXPECTED, ERROR_MESSAGE
assert notebook2.exit_values.get('test_list_key') == EXPECTED, ERROR_MESSAGE
assert Notebook.exit_values.get('test_list_key') == EXPECTED, ERROR_MESSAGE

notebook.exit()
