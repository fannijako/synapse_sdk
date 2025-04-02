## DataProduct Class Documentation
### Overview

The `DataProduct` class is designed to manage data products by handling curated and trusted tables. It provides methods for optimizing and vacuuming these tables.

The `DataProduct` class is a subclass of `Notebook`.

### Attributes
#### Required parameters
--

#### Optional parameters
--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **curated_tables**:
  - cached attribute
  - constructed using the Util's module's get_all_deltas() method
  - A dictionary containing curated tables.

- **trusted_tables**:
  - cached attribute
  - constructed using the Util's module's get_all_deltas() method
  - A dictionary containing trusted tables.

### Methods

#### `__init__() -> DataProduct`
Initializes an `DataProduct` instance.

It sets the `curated_tables` and `trusted_tables` attributes.

#### `__eq__(other_data_product: DataProduct) -> bool`
Checks if two `DataProduct` instances are equal based on their type and Azure storage account name.

#### `__contains__(table: str) -> bool`
Determines if a table is present in either the curated or trusted tables.

#### `__str__() -> str`
Returns a string representation of the data product, including its name and version.

#### `__repr__() -> str`
Returns a string representation of the object type.

#### `optimize_all(layer: str = 'curated', partition_filter: str = None) -> None`
Optimizes delta tables in specified layers. If no layer is specified, it optimizes both curated and trusted layers.

- **Parameters**:
  - `layer`: The layer to optimize. Defaults to `'curated'`.
  - `partition_filter`: Optional filter for partitions.

- **Example Usage**:
  ```python
  DataProduct().optimize_all()
  ```

#### `vacuum_all(layer: str = 'curated', hours: int = 168, force: bool = False) -> None`
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
