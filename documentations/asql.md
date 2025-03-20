## AsqlDatabase Class Documentation
### Overview

The `AsqlDatabase` class represents an Azure SQL Database and is a subclass of `Notebook`. It encapsulates properties and methods necessary for interacting with Azure SQL databases.

### Attributes

- **database_name**: The name of the Azure SQL database.
- **database_schema**: The schema within the database.
- **database_server**: The server hosting the database, constructed based on the environment and data product name.
- **linked_service_name**: The name of the linked service for the database.

### Methods

#### `__init__(database_name: str, database_schema: str)`

Initializes an `AsqlDatabase` instance. It sets the `database_name`, `database_schema`, constructs the `database_server` based on the environment, and defines the `linked_service_name`.

#### `__eq__(other_database) -> bool`

Checks if two `AsqlDatabase` instances are equal based on their type, `database_server`, `database_name`, `database_schema`, and `linked_service_name`.

#### `__str__() -> str`

Returns a string representation of the Azure SQL database linked service.

#### `__repr__() -> str`

Returns a string representation that could be used to recreate the object.

#### `get_token() -> str`

Retrieves the connection string token for the linked service.

#### `build_connection_properties(database_table: str) -> Tuple[dict, str, str]`

Constructs connection properties for a specific database table. It returns a dictionary with connection details, the JDBC URL, and the fully qualified database table name.

### Example Usage

```python
# Create an instance of AsqlDatabase
database = AsqlDatabase("my_database", "my_schema")

# Get the connection token
token = database.get_token()

# Build connection properties for a table
connection_properties, url, dbtable = database.build_connection_properties("my_table")
```

### Notes

- 
