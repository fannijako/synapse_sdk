## SynStorageAccount Documentation
### Overview

The `SynStorageAccount` class represents the Synapse default ADLSGen2 service.

The `SynStorageAccount` class is a subclass of `Notebook`.

### Attributes

#### Required parameters
--

#### Optional parameters
--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **linked_service_name**: The name of the linked service for the storage account.
    - constructed based on the data product name and version
    - e.g. dlssyntisc002

### Methods
#### `__init__() -> SynStorageAccount`

Initializes an `SynStorageAccount` instance.

It sets the `linked_service_name` based on the data product name and version.

#### `__eq__(other_syn_storage: SynStorageAccount) -> bool`

Checks if two `SynStorageAccount` instances are equal based on their instance type and `linked_service_name` attributes.

#### `__str__() -> str`

Returns a string representation of the Synapse default ADLSGen2 service.

#### `__repr__() -> str`

Returns a string representation that could be used to recreate the object.

### Example Usage

```python
syn_account = SynStorageAccount()
print(syn_account.linked_service_name)
```
