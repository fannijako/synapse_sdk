## LHTSparkDataFrame Documentation
### Overview

The `LHTSparkDataFrame` class is a subclass of `DataPlaceholder`, designed to handle Spark DataFrames with additional functionalities for versioning, timestamp management, and data manipulation.

### Attributes

- **file_format**: The file format used, which is set to `'delta'`.
- **version**: The version of the DataFrame, represented as a `PositiveNumber`.
- **timestamp**: A string representing the timestamp or `None`.
- **name**: The name of the DataFrame.
- **load_type**: The type of data loading, which can be `None`.
- **layer**: The layer in which the DataFrame resides, defaulting to `'curated'`.
- **latest_version**: The latest version available.
- **dataframe**: The actual Spark DataFrame object.

### Methods

#### Initialization

- **`__init__(name: str, load_type: str = None, layer: str = 'curated', version: int = None, timestamp: str = None)`**: Initializes the `LHTSparkDataFrame` object.

#### Comparison and Arithmetic Operations

- **`__eq__(other_dataframe) -> bool`**: Checks if two DataFrames are equal based on type, super class equality, and version.
- **`__lt__(other_dataframe) -> bool`**, **`__le__(other_dataframe) -> bool`**, **`__gt__(other_dataframe) -> bool`**, **`__ge__(other_dataframe) -> bool`**: Compares versions between DataFrames.
- **`__add__(version_increase: int)`**, **`__sub__(version_decrease: int)`**: Increases or decreases the version of the DataFrame.

#### String Representations

- **`__str__() -> str`**: Returns a human-readable string representation of the DataFrame.
- **`__repr__() -> str`**: Returns a more formal string representation for debugging.

#### Data Loading and Management

- **`load_dataframe() -> tuple[DataFrame, int, str]`**: Loads the DataFrame based on version or timestamp.
- **`get_timestamp_of_version() -> str`**: Retrieves the timestamp of a specific version.
- **`get_version_of_timestamp() -> int`**: Retrieves the version of a specific timestamp.
- **`get_latest_version() -> int`**: Retrieves the latest version available.

#### Data Manipulation

- **`add_timestamp_column(timestamp_column_name: str = "load_timestamp", timezone: str = None, timestamp_format: str = 'yyyy-MM-dd HH:mm:ss') -> None`**: Adds a timestamp column to the DataFrame.
- **`add_hash_column(prefix: str = 'dap') -> None`**: Adds a hash column to the DataFrame by concatenating all columns and applying SHA-256 hashing.
- **`rename_columns_w_pattern(pattern_to_replace: str, replace_to: str = "") -> None`**: Renames columns based on a pattern.
- **`rename_columns_w_mapping(column_names: dict) -> None`**: Renames columns using a mapping dictionary.
- **`cast_data_columns(column_types: dict) -> None`**: Casts columns to specified types.

#### Data Analysis

- **`is_changed_since_last_version(columns_to_ignore: list = None) -> bool`**: Checks if the DataFrame has changed since the last version.

#### Data Writing

- **`write_to_database(database_name: str, database_schema: str, table_name: str = None, create_table_statement: str = "", mode: str = 'auto')`**: Writes the DataFrame to a database.
- **`write_to_excel(target_path: str) -> None`**: Writes the DataFrame to an Excel file.

#### Utilities

- **`history(limit: int = 10)`**: Retrieves the history of the Delta table.
- **`construct_merge_condition(primary_keys: list, source: str = 'src', sink: str = 'dst', are_nulls_matched: bool = True) -> str`**: Constructs a merge condition string based on primary keys.

### Example Usage

```python
# Initialize a new LHTSparkDataFrame
df = LHTSparkDataFrame(name="example_table", load_type="scd1", layer="curated")

# Load the DataFrame with the latest version
df.load_dataframe()

# Add a timestamp column
df.add_timestamp_column(timestamp_column_name="load_time")

# Write the DataFrame to a database
df.write_to_database(database_name="my_database", database_schema="public")

# Write the DataFrame to an Excel file
df.write_to_excel(target_path="abfss://path/to/output.xlsx")
```

### Notes

- Ensure that the `spark` and `mssparkutils` modules are properly configured and imported.
- The `AsqlDatabase` class and its methods should be defined elsewhere in your codebase.
- The `DataPlaceholder` class and its methods should be defined elsewhere in your codebase.
