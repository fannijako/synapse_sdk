## DataPlaceholder and Table Classes Documentation
### Overview

The `DataPlaceholder` class serves as a base class for managing data structures like tables and data frames.

It is subclassed by the `Table` class, as well as the `LHTSparkDataFrame` class, which provides additional functionality specific to table and dataframe operations.

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

### Table Class

#### Description

The `Table` class extends the `DataPlaceholder` class and is specifically designed for table operations. It includes additional attributes and methods for managing table properties and performing optimizations.

#### Attributes
#### Inherited attributes
- All attributes of a DataPlaceholder class, see above.

#### Class attributes
--

#### Additional attributes
- **table_size**: The delta lake table size in bytes
    - using the DESCRIBE DETAIL command

- **target_file_size**: The recommended file size for table optimization in MB
    - The target file size for rewrites value based on the followint recommendations:
        - 128 MB - below 10 GB
        - 256 MB - below 3 TB
        - 512 MB - below 10 TB
        - 1 GB - above 10 TB
    - Returns value in a format that can be used with the spark configuration settings

- **delta_table**: A DeltaTable object representing the table.
    - read only attribute

- **dataframe**: A Spark DataFrame object representing the table's data.
    - read only attribute

#### Methods
#### `__init__(name: str, load_type: str = None, layer: str = 'curated') -> Table`

Initializes an `Table` instance.

It sets all attributes.

#### `__str__() -> str`
Returns a string representation of the Table.

#### `__repr__() -> str`
Returns a string representation that could be used to recreate the object.

#### `calculate_table_properties()`:
Calculates the table's size and target file size.
- Sets all attributes.
- Called in the init method.

#### `get_target_table_size() -> float`:
Retrieves the table size in bytes from the 
- Called in the calculate_table_properties() method.
- Sets the table_size attribute.

#### `calculate_target_file_size() -> str`:
Calculates the optimal file size based on the table size.
- Called in the calculate_table_properties() method.
- Sets the target_file_size attribute.

#### `vacuum(hours: int = 168, force: bool = False) -> None`:
Performs a vacuum operation on the table.

- **Parameters**:
  - `hours` (int, optional): retention value in VACUUMing in hours. Defaults to 168 (hours) = 7 days
  - `force` (bool, optional): Force the VACUUMing below 7 days.

#### `zorder(columns: list, partition_filter: str = None) -> None`:
Executes Z-ORDER BY on the table.

- **Parameters**:
  - `columns` (list): column names to use the ZORDER on
  - `partition_filter(str, optional)`: Partition filters to apply during the ZORDER

#### `optimize(partition_filter: str = None) -> None`:
Compacts the table. Executes OPTIMIZE on the table.

- **Parameters**:
  - `partition_filter(str, optional)`: Partition filters to apply during the OPTIMIZE

#### `history(limit: int = 10) -> DataFrame`:
Retrieves the table's history.

- **Parameters**:
  - `limit` (int, optional): Number of past operations to return
- **Returns**: Spark DataFrame object

#### `calculate_enforce_save_target_table_metadata() -> None`:
Sets table properties for optimization
- to the targetFileSize and enable autooptimize.optimizeWrite for later writes

#### `calculate_zorder_and_analyse_columns(primary_keys: list[str]) -> tuple[list[str]]`:
Identifies columns for Z-ORDER BY and analysis.

- Select column candidates for Z-ORDER BY and ANALYZE from the primary keys
- Specifications for Z-ORDER BY:
            - returns at most 4 columns
            - returns only high cardinality columns
                threshold: 0.01%
                statistic: number of distinct values / number of rows
                threshold: 10 distinct values
- Specification for ANALYZE:
            - primary key
            - not Z-ORDER BY
            - more than 1 distinct values

- **Parameters**:
  - `primary_keys (list[str])`: list of primary keys of the table.

- **Returns**: 
    - list[str]: list of column names to use in Z-ORDERING.
    - list[str]: list of column names to calculate statistics about other than the Z-ORDERING columns.

#### `calculate_statistics(primary_keys: list[str] = None) -> tuple[str, str, int, int]`:
Calculate the following statistics:
    - z-order columns
    - analyse columns
    - number of columns to calculate statistics on

- **Parameters**:
  - `primary_keys (list[str])`: list of primary keys of the table.

#### `set_table_properties()`:
Sets table properties for optimization.
- Executes the `self.calculate_enforce_save_target_table_metadata()` and the `self.calculate_statistics()` methods

#### `get_optimization_recommendations()`:
Provides optimization recommendations. E.g. run an optimize, run a vacuum or use the following spark configs while reading

### Example Usage

```python
# Create a Table instance
my_table = Table("my_table_name")

# Calculate and set table properties
my_table.set_table_properties()

# Perform optimization
my_table.optimize()

# Get optimization recommendations
print(my_table.get_optimization_recommendations())
```

### Notes
- Module uses the Delta Lake Python API extensively.
