## DataProduct Class Documentation
### Overview

The `DataProduct` class is a subclass of `Notebook`, designed to manage data products by handling curated and trusted tables. It provides methods for optimizing and vacuuming these tables.

### Attributes

- **curated_tables**: A dictionary containing curated tables.
- **trusted_tables**: A dictionary containing trusted tables.

### Methods

#### `__init__`
Initializes a `DataProduct` instance by calling the parent class's constructor and referencing the `curated_tables` and `trusted_tables` attributes.

#### `__eq__`
Checks if two `DataProduct` instances are equal based on their type and Azure storage name.

#### `__contains__`
Determines if a table is present in either the curated or trusted tables.

#### `__str__`
Returns a string representation of the data product, including its name and version.

#### `__repr__`
Returns a string representation of the object type.

#### `curated_tables`
A cached property that retrieves all delta tables from the curated path.

#### `trusted_tables`
A cached property that retrieves all delta tables from the trusted path.

#### `optimize_all`
Optimizes delta tables in specified layers. If no layer is specified, it optimizes both curated and trusted layers.

- **Parameters**:
  - `layer`: The layer to optimize. Defaults to `'curated'`.
  - `partition_filter`: Optional filter for partitions.

- **Example Usage**:
  ```python
  DataProduct().optimize_all()
  ```

#### `vacuum_all`
Vacuums delta tables in specified layers. If no layer is specified, it vacuums both curated and trusted layers.

- **Parameters**:
  - `layer`: The layer to vacuum. Defaults to `'curated'`.
  - `hours`: Retention period in hours. Defaults to `168` (7 days).
  - `force`: Whether to force vacuuming. Defaults to `False`.

- **Example Usage**:
  ```python
  DataProduct().vacuum_all()
  ```

### Example Use Cases

```python
# Create a DataProduct instance
data_product = DataProduct()

# Check if a table exists
if "my_table" in data_product:
    print("Table exists")

# Optimize all tables in the curated layer
data_product.optimize_all()

# Vacuum all tables in the trusted layer with a retention period of 7 days
data_product.vacuum_all(layer='trusted', hours=168)
```

### Notes

- The `DataProduct` class relies on the `Notebook` class and uses methods like `get_all_deltas` which are not defined in this snippet.
- The `Table` class is used to interact with individual tables, but its definition is not provided here.
- The `spark` object is assumed to be available for configuring Spark settings.
