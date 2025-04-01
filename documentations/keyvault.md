## KeyVault Class Documentation
### Overview

The `KeyVault` class represents an Azure Key Vault service.

The `KeyVault` class is a subclass of `Notebook`.

### Attributes

#### Required parameters
--

#### Optional parameters
--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **linked_service_name**: The name of the linked service for the Key Vault.
    - constructed based on the data product name and version
    - e.g. kvtisc002
- **key_vault_name**: The name of the Key Vault.
    - constructed based on the data product name, version and environment
    - e.g. kv-tisc-d-002

### Methods
#### `__init__() -> KeyVault`
Initializes a new instance of the `KeyVault` class.

It sets the `linked_service_name` and `key_vault_name` based on the `data_product_name`, `data_product_version`, and `environment`.

#### `__eq__(other_keyvault: KeyVault) -> bool`
Checks if two `KeyVault` instances are equal based on their type and `linked_service_name`.

#### `__str__(): -> str`
Returns a string representation of the `KeyVault` instance, including its linked service name.

#### `__repr__(): -> str`
Returns a string representation of the object type.

#### `get_secret(secret_name: str) -> str`
Retrieves a secret from the Key Vault using mssparkutils.credentials.

- **Parameters**:
  - `secret_name`: The name of the secret to retrieve.
- **Returns**: The value of the secret as a string.

#### `put_secret(secret_name: str, secret_value: str) -> None`
Stores a secret in the Key Vault using mssparkutils.credentials.

- **Parameters**:
  - `secret_name`: The name of the secret to store.
  - `secret_value`: The value of the secret to store.
- **Returns**: None

### Example Usage
```python
key_vault = KeyVault()

# Retrieve a secret
secret_value = key_vault.get_secret("my_secret")

# Store a secret
key_vault.put_secret("new_secret", "secret_value")
```

### Notes
- The `mssparkutils.credentials` module is used for interacting with Key Vault secrets, which is specific to Azure Synapse Analytics environments.
