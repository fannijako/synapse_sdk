## Notebook Class Documentation
### Overview

The `Notebook` class is a subclass of `Utils` designed to manage and provide context for notebooks in a data processing environment. It includes attributes for workspace, data product, environment, and paths to various storage locations. The class also offers methods for setting Spark datetime settings, managing exit values, and exiting the notebook.

### Attributes

- **`exit_values`**: A class-level dictionary to store exit values.
- **`workspace_name`**: The name of the workspace where the notebook is running.
- **`data_product_name`**: The name of the data product associated with the notebook.
- **`environment`**: The environment type (e.g., 'p' for production, 'd' for development).
- **`data_product_version`**: The version of the data product.
- **`notebook_name`**: The name of the current notebook.
- **`job_id`**: The ID of the job running the notebook.
- **`pipeline_job_id`**: The ID of the pipeline job if applicable.
- **`pool`**: The name of the pool used by the notebook.
- **`cluster`**: The ID of the cluster running the notebook.
- **`azure_storage_name`**: The name of the Azure storage account.
- **`curated_path`**, **`standardized_curated_path`**, **`sensitive_standardized_curated_path`**, **`trusted_path`**: Paths to different data storage locations.
- **`resource_group`**: The resource group associated with the notebook.
- **`session_notebook_name`**: The name of the notebook in the current session.
- **`session_run_id`**: The run ID of the session.

### Methods

#### Initialization
- **`__init__`**: Initializes the notebook object by setting up attributes and paths based on the workspace name.

#### Properties
- **`workspace_name`**, **`data_product_name`**, **`environment`**, **`data_product_version`**, **`notebook_name`**, **`job_id`**, **`pipeline_job_id`**, **`pool`**, **`cluster`**, **`azure_storage_name`**, **`curated_path`**, **`standardized_curated_path`**, **`sensitive_standardized_curated_path`**, **`trusted_path`**, **`resource_group`**, **`session_notebook_name`**, **`session_run_id`**: Getters for the respective attributes.

#### Setters
- **`data_product_name`**, **`environment`**, **`data_product_version`**: Setters that update the respective attributes and recalculate paths. Note that `azure_storage_name`, `curated_path`, `standardized_curated_path`, `sensitive_standardized_curated_path`, and `trusted_path` cannot be set manually.

#### Utilities
- **`set_spark_datetime_settings`**: Configures Spark to handle datetime correctly.
- **`set_exit_value`**: Sets or extends exit values for the notebook.
- **`exit`**: Exits the notebook with the previously set exit values.
- **`get_connection_string_or_creds`**: Retrieves connection string or credentials for a linked service (only applicable to subclasses with a `linked_service_name` attribute).

#### Comparison
- **`__eq__`**: Compares two notebooks based on their attributes.

#### Representation
- **`__str__`**: Returns a string representation of the notebook.
- **`__repr__`**: Returns a basic representation of the notebook object.

### Example Usage

```python
# Initialize a Notebook object
notebook = Notebook()

# Set an exit value
Notebook.set_exit_value('status', 'success')

# Exit the notebook
notebook.exit()

# Access attributes
print(notebook.workspace_name)
print(notebook.data_product_name)
```

### Notes

- The `data_product_name`, `environment`, and `data_product_version` attributes are initially derived from the workspace name and can be updated manually.
- Paths (`azure_storage_name`, `curated_path`, etc.) are recalculated based on changes to `data_product_name`, `environment`, and `data_product_version`.
- The `exit_values` dictionary is used to store exit information for the notebook.
