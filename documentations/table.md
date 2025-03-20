## DataPlaceholder and Table Classes Documentation
### Overview

The `DataPlaceholder` class serves as a base class for managing data structures like tables and data frames. It is subclassed by the `Table` class, which provides additional functionality specific to table operations.

### DataPlaceholder Class

#### Description

The `DataPlaceholder` class is designed to handle basic data placeholder operations. It includes attributes for `name`, `load_type`, and `layer`, which are essential for identifying and managing data sources.

#### Attributes

- **`name`**: The name of the data placeholder.
- **`load_type`**: The type of data loading, which can be specified or determined automatically.
- **`layer`**: The layer in which the data is stored, either 'curated' or 'trusted'.

#### Methods

- **`__init__(name: str, load_type: str = None, layer: str = 'curated')`**: Initializes a `DataPlaceholder` instance.
- **`_find_path()`**: Finds the path to the data based on its name and layer.
- **`__eq__(other_table)`**: Checks if two `DataPlaceholder` instances are equal based on their type, name, and layer.

### Table Class

#### Description

The `Table` class extends the `DataPlaceholder` class and is specifically designed for table operations. It includes additional attributes and methods for managing table properties and performing optimizations.

#### Attributes

- **`name`**: Inherited from `DataPlaceholder`.
- **`load_type`**: Inherited from `DataPlaceholder`.
- **`layer`**: Inherited from `DataPlaceholder`.
- **`table_size`**: The size of the table in bytes.
- **`target_file_size`**: The recommended file size for table optimization.
- **`delta_table`**: A DeltaTable object representing the table.
- **`dataframe`**: A DataFrame object representing the table's data.

#### Methods

- **`__init__(name: str, load_type: str = None, layer: str = 'curated')`**: Initializes a `Table` instance and calculates its properties.
- **`calculate_table_properties()`**: Calculates the table's size and target file size.
- **`get_target_table_size()`**: Retrieves the table size in bytes.
- **`calculate_target_file_size()`**: Calculates the optimal file size based on the table size.
- **`vacuum(hours: int = 168, force: bool = False)`**: Performs a vacuum operation on the table.
- **`zorder(columns: list, partition_filter: str = None)`**: Executes Z-ORDER BY on the table.
- **`optimize(partition_filter: str = None)`**: Compacts the table.
- **`history(limit: int = 10)`**: Retrieves the table's history.
- **`calculate_enforce_save_target_table_metadata()`**: Sets table properties for optimization.
- **`calculate_zorder_and_analyse_columns(primary_keys: list[str])`**: Identifies columns for Z-ORDER BY and analysis.
- **`calculate_statistics(primary_keys: list[str] = None)`**: Calculates statistics for the table.
- **`set_table_properties()`**: Sets table properties for optimization.
- **`get_optimization_recommendations()`**: Provides optimization recommendations.

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

- The `Table` class relies on Spark for operations like reading and optimizing Delta tables.
- The `load_type` is determined based on the most common operation type in the table's history.
- The `target_file_size` is calculated based on the table size to optimize storage and performance.