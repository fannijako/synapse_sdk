## DataPlaceholder and LHTSparkDataFrame Classes Documentation
### Overview

The `DataPlaceholder` class serves as a base class for managing data structures like tables and data frames.

It is subclassed by the `LHTSparkDataFrame` class, as well as the `Table` class, which provides additional functionality specific to table and dataframe operations.

### DataPlaceholder Class

#### Description

The `DataPlaceholder` class is designed to handle basic data placeholder operations. It includes attributes for `name`, `load_type`, and `layer`.

#### Attributes
#### Required parameters
- **name**: The name of the table
    - read only after initialization
    - e.g. zkpa_kalk_stat for the zkpa_kalk_stat.delta delta lake

#### Optional parameters
- **load_type**: The type of data loading
    - can be specified or determined automatically
    - either full or scd1
    - calculated based on the most common write operation type (MERGE or OWERWRITE) within the table history if set automatically

- **layer**: The layer in which the data is stored
    - read only after initialization
    - either 'curated' or 'trusted'
    - defaults to curated

#### Inherited attributes
- All attributes of a DataProduct class, see in `dataproduct.md`.

#### Additional attributes
- **path**: abfss path to the delta lake
    - set by the _find_path() method within the initialization
    - read only attribute

#### Methods

#### `__init__(name: str, load_type: str = None, layer: str = 'curated') -> DataPlaceholder`:
Initializes a `DataPlaceholder` instance.

It sets all attributes and searches the path with the `_find_path()` method to the specific delta lake.

#### `_find_path() -> str`:
Finds the path to the data based on its name and layer.

#### `__eq__(other_table: DataPlaceholder) -> bool`:
Checks if two `DataPlaceholder` instances are equal based on their type, name, and layer. Evaluates to True on a Table and an LHTSparkDataFrame over the same Delta Lake.


## LHTSparkDataFrame Class

### Description

The `LHTSparkDataFrame` class extends the `DataPlaceholder` class and is specifically designed for Spark dataframe operations, e.g. additional functionalities for versioning, timestamp management, and data manipulation.

### Attributes
#### Inherited attributes
- All attributes of a DataPlaceholder class, see above.

#### Class attributes
- **file_format**: The file format used, which is set to `'delta'`.

#### Optional attributes
- **version**: The version of the DataFrame.
    - used in read operation

- **timestamp**: Timestamp to read the version of the Table of.
    - used in read operation

#### Additional attributes
- **delta_table**: Table object, see details in `table.md`
    - read only

- **latest_version**: The latest version available on the delta lake.
    - calculated based on the HISTORY command on the table

- **dataframe**: The actual Spark DataFrame object.
    - read only

### Methods

#### `__init__(name: str, load_type: str = None, layer: str = 'curated', version: int = None, timestamp: str = None) -> LHTSparkDataFrame`:
Initializes the `LHTSparkDataFrame` object.

#### `__eq__(other_dataframe: LHTSparkDataFrame) -> bool`:
Checks if two DataFrames are equal based on type, super class equality, and version.

#### `__lt__(other_dataframe: LHTSparkDataFrame) -> bool`:
Compares versions between DataFrames based on type, super class equality, and version.

#### `__le__(other_dataframe: LHTSparkDataFrame) -> bool`:
Compares versions between DataFrames based on type, super class equality, and version.

#### `__gt__(other_dataframe: LHTSparkDataFrame) -> bool`:
Compares versions between DataFrames based on type, super class equality, and version.

#### `__ge__(other_dataframe: LHTSparkDataFrame) -> bool`:
Compares versions between DataFrames based on type, super class equality, and version.

#### `__add__(version_increase: int)`:
Increases the version of the DataFrame.

#### `__sub__(version_decrease: int)`:
Decreases the version of the DataFrame.

#### `__str__() -> str`:
Returns a human-readable string representation of the DataFrame.

#### `__repr__() -> str`:
Returns a string representation that could be used to recreate the object.

#### `load_dataframe() -> tuple[DataFrame, int, str]`:
Loads the DataFrame based on version or timestamp.

#### `get_timestamp_of_version() -> str`:
Retrieves the timestamp of a specific version.

#### `get_version_of_timestamp() -> int`:
Retrieves the version of a specific timestamp.

#### `get_latest_version() -> int`:
Retrieves the latest version number available.

#### `is_changed_since_last_version(columns_to_ignore: list = None) -> bool`:
Checks if the DataFrame has changed since the last version other than the columns secified.

- **Parameters**:
  - `columns_to_ignore` (list, optional): columns to ignore in the comparison, e.g. the DAP technical columns, like __loadTimestampCurated

#### `write_to_database(database_name: str, database_schema: str, table_name: str = None, create_table_statement: str = "", mode: str = 'auto')`:
Writes the DataFrame to a database.

- **Parameters**:
  - `database_name` (str): Name of the database
  - `database_schema` (str):  Name of the schema in the database
  - `table_name` (str, optional): Name of the table. If None, table name of the delta lake will be used. Defaults to None.
  - `create_table_statement` (str, optional): Additional SQL query to run after ingestion, e.g. ALTER TABLE statements. Defaults to None
  - `mode` (str, optional): Mode to use during write: append or overwrite. If set to auto, the mode will be determined based on the load_type of the delta lake. Defaults to auto.

#### `add_timestamp_column(timestamp_column_name: str = "load_timestamp", timezone: str = None, timestamp_format: str = 'yyyy-MM-dd HH:mm:ss') -> None`:
Adds a timestamp column to a PySpark DataFrame with an optional timezone and custom format.

- **Parameters**:
  - `timestamp_column_name` (str, optional): Name of the column to add. Defaults to load_timestamp.
  - `timezone` (str, optional): Timezone to use for the values. Defaults to None.
  - `timestamp_format` (str, optional): Timestamp format to use for the values. Defaults to 'yyyy-MM-dd HH:mm:ss'

#### `add_hash_column(prefix: str = 'dap') -> None`:
Add a hash column to a Spark DataFrame by concatenating all columns and applying SHA-256 hashing. The name of the hash column will be based on the provided prefix (e.g., 'dap_hash' for 'dap' prefix).

This function concatenates all columns of the input DataFrame into a single string for each row, applies SHA-256 hashing to these strings, and adds the hash as a new column. 

The name of this new column is constructed using the given prefix followed by '_hash'.

- **Parameters**:
  - `prefix` (str, optional): Prefix to the column name to add, e.g. dap will return dap_has. Defaults to dap.

#### `rename_columns_w_pattern(pattern_to_replace: str, replace_to: str = "") -> None`:
Rename the column names based on the given pattern. It removes the pattern by default.

- **Parameters**:
  - `pattern_to_replace` (str): The string pattern to replace.
  - `replace_to` (str, optional): The new string. Defaults to ''.

#### `rename_columns_w_mapping(column_names: dict) -> None`:
Apply the renaming to each column in the dictionary.

- **Parameters**:
  - `column_names` (dict): The mapping dictionary. 
        Example:
                df_mapping = {
                    'current_col_name': 'new_col_name',
                    'current_col_name2': 'new_col_name2'
                }

#### `cast_data_columns(column_types: dict) -> None`:
Apply the casting to each column in the dictionary.

- **Parameters**:
  - `column_types` (dict): The column types dictionary.
        Example:
                df_cast = {
                    'col_name': IntegerType(),
                    'col_name2': StringType()
                }

#### `history(limit: int = 10)`
Retrieves the history of the Delta table.

- **Parameters**:
  - `limit` (int): Number of operations to return

#### `construct_merge_condition(primary_keys: list, source: str = 'src', sink: str = 'dst', are_nulls_matched: bool = True) -> str`:
Constructs a merge condition string based on primary keys.

- **Parameters**:
  - `primary_keys` (list): List of primary keys of the table.
  - `source` (str, optional): Name to use for source. Defaults to src.
  - `sink` (str, optional):  Name to use for sink. Defaults to dst.
  - `are_nulls_matched` (bool, optional): Whether to match null values with null values.

#### `write_to_excel(target_path: str) -> None`:
Write the joined data to the target path in Excel format

- **Parameters**:
    - `target_path` (str): abfss:// path to write the result to

### Example Usage

```python
# Initialize a new LHTSparkDataFrame
df = LHTSparkDataFrame(name="example_table", load_type="scd1", layer="curated")

# Add a timestamp column
df.add_timestamp_column(timestamp_column_name="load_time")

# Write the DataFrame to a database
df.write_to_database(database_name="my_database", database_schema="public")

# Write the DataFrame to an Excel file
df.write_to_excel(target_path="abfss://path/to/output.xlsx")
```
