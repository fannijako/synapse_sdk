## KeyVault Class Documentation
### Overview
The `KeyVault` class is a subclass of `Notebook`, designed to manage interactions with Azure Key Vault services. It provides methods for retrieving and storing secrets securely.

### Attributes
- **linked_service_name**: A string attribute that represents the name of the linked service for the Key Vault.

### Methods
#### `__init__`
Initializes a new instance of the `KeyVault` class. It calls the parent class's constructor and sets the `linked_service_name` and `key_vault_name` based on the `data_product_name`, `data_product_version`, and `environment`.

#### `__eq__`
Checks if two `KeyVault` instances are equal based on their type and `linked_service_name`.

#### `__str__`
Returns a string representation of the `KeyVault` instance, including its linked service name.

#### `__repr__`
Returns a string representation of the object type.

#### `get_secret`
Retrieves a secret from the Key Vault.

- **Parameters**:
  - `secret_name`: The name of the secret to retrieve.
- **Returns**: The value of the secret as a string.

#### `put_secret`
Stores a secret in the Key Vault.

- **Parameters**:
  - `secret_name`: The name of the secret to store.
  - `secret_value`: The value of the secret to store.
- **Returns**: None

### Example Usage
```python
# Create a new KeyVault instance
key_vault = KeyVault()

# Retrieve a secret
secret_value = key_vault.get_secret("my_secret")

# Store a secret
key_vault.put_secret("new_secret", "secret_value")
```

### Notes
- The `data_product_name`, `data_product_version`, and `environment` are assumed to be defined elsewhere in the codebase, as they are used in the `__init__` method.
- The `mssparkutils.credentials` module is used for interacting with Key Vault secrets, which is specific to Azure Synapse Analytics environments.
