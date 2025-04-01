## Kusto Class Documentation
### Overview

The `Kusto` class represents an Azure Data Explorer (Kusto) service.

The `Kusto` class is a subclass of `Notebook`.

### Attributes

#### Required parameters
--

#### Optional parameters
--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **linked_service_name**: The name of the linked service for the service.
    - constructed based on the data product name and version
    - e.g. dectisc002

### Methods
#### `__init__() -> Kusto`

Initializes an `Kusto` instance.

It sets the `linked_service_name` based on the data product name and version.

#### `__eq__(other_kusto: Kusto) -> bool`

Checks if two `Kusto` instances are equal based on their instance type, and `linked_service_name` attributes.

#### `__str__() -> str`

Returns a string representation of the Kusto linked service.

#### `__repr__() -> str`

Returns a string representation that could be used to recreate the object.

### Example Usage
```python
kusto_instance = Kusto()
print(kusto_instance.linked_service_name)
```
