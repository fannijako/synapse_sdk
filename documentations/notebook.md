## Notebook Class Documentation
### Overview

The `Notebook` class is designed to manage and provide context for notebooks in a data processing environment. It includes attributes for workspace, data product, environment, and paths to various storage locations. The class also offers methods for setting Spark datetime settings, managing exit values, and exiting the notebook.

The `Notebook` class is a subclass of `Utils`.

### Attributes
#### Required parameters
--

#### Optional parameters
--

#### Inherited attributes
--

#### Class attributes
- **exit_values**: A class-level dictionary to store exit values.

#### Additional attributes
- **workspace_name**: The name of the workspace where the notebook is running.
    - read only attribute
    - constructed using mssparkutils.env
    - e.g. syn-tisc-d-002

- **data_product_name**: The name of the data product associated with the notebook.
    - constructed from the workspace_name
    - e.g. tisc

- **environment**: The environment type 
    - 'p' for production, 'd' for development
    - constructed from the workspace_name
    - e.g. d

- **data_product_version**: The version of the data product.
    - constructed from the workspace_name
    - e.g. 002

- **azure_storage_name**: The name of the Azure storage account.
    - read only attribute
    - constructed based on the environment, data product name and version
    - e.g. dlstiscd002

- **curated_path**: Paths to the curated container in the storage account.
    - read only attribute
    - constructed based on the azure_storage_name
    - e.g. abfss://curated@dlstiscd002.dfs.core.windows.net

- **standardized_curated_path**: Paths to the standardized layer in the curated container in the storage account.
    - read only attribute
    - constructed based on the azure_storage_name
    - e.g. abfss://curated@dlstiscd002.dfs.core.windows.net/standardized

- **sensitive_standardized_curated_path**: Paths to the sensitive-standardized layer in the curated container in the storage account.
    - read only attribute
    - constructed based on the azure_storage_name
    - e.g. abfss://curated@dlstiscd002.dfs.core.windows.net/sensitive-standardized

- **trusted_path**: Paths to the trusted container in the storage account.
    - read only attribute
    - constructed based on the azure_storage_name
    - e.g. abfss://trusted@dlstiscd002.dfs.core.windows.net

- **notebook_name**: The name of the current notebook.
    - read only attribute
    - constructed using mssparkutils.runtime
    - e.g. generic_utils

- **job_id**: The ID of the job running the notebook.
    - read only attribute
    - constructed using mssparkutils.env

- **pipeline_job_id**: The ID of the pipeline job if applicable.
    - read only attribute
    - constructed using mssparkutils.runtime

- **pool**: The name of the pool used by the notebook.
    - read only attribute
    - constructed using mssparkutils.env
    - e.g. synsptiscs

- **cluster**: The ID of the cluster running the notebook.
    - read only attribute
    - constructed using mssparkutils.env

- **resource_group**: The resource group associated with the data product.
    - read only attribute
    - constructed based on the environment, data product name and version
    - e.g. rg-ds-tisc-d-002

- **session_notebook_name**: The name of the notebook in the current session.
    - read only attribute
    - extracted from spark configuration values

- **session_run_id**: The run ID of the session.
    - read only attribute
    - constructed from session_notebook_name


### Methods
#### `__init__() -> Notebook`

Initializes an `Notebook` instance.

It sets all attributes and the datetime related spark configuration values.

#### `__eq__(other_notebook: Notebook) -> bool`

Checks if two `Notebook` instances are equal based on their instance type and attributes.

#### `__str__() -> str`

Returns a string representation of the Notebook.

#### `__repr__() -> str`

Returns a string representation that could be used to recreate the object.

#### `set_spark_datetime_settings() -> None`
Configures Spark to handle datetime correctly. Runs during initialization.

```python
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead" , "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead"    , "CORRECTED")
spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite"   , "CORRECTED")
```

#### `_construct_paths() -> None`
Reconstruct paths after change of data product name, version or environment. Called automatically after attribute changes.

#### `set_exit_value() -> None`
Sets or extends exit values for the notebook.
    Set:
        - if key did not exist yet
        - if key did exist and was a string
    Extend:
        - if key did exist and was a list and the new one is a list (extend)
        - if key did exist and was a list and the new one is a string (append)

#### `get_connection_string_or_creds() -> str`
Retrieves connection string or credentials for a linked service (only applicable to subclasses with a `linked_service_name` attribute).
- constructs value based on mssparkutils.credentials

#### `exit() -> None`:
Exits the notebook with the previously set exit values.
- Uses the mssparkutils.notebook.exit module

### Example Usage

```python
notebook = Notebook()
notebook.set_exit_value('status', 'success')

# Access attributes
print(notebook.workspace_name)
print(notebook.data_product_name)

notebook.exit()
```

### Notes

- The `data_product_name`, `environment`, and `data_product_version` attributes are initially derived from the workspace name and can be updated manually.
- Paths (`azure_storage_name`, `curated_path`, etc.) are recalculated based on changes to `data_product_name`, `environment`, and `data_product_version`.
- The `exit_values` dictionary is used to store exit information for the notebook.
- The `mssparkutils` module and the `spark.conf.get` configuration values are used for retrieving the attributes.

