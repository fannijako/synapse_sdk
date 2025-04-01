## AsqlDatabase Class Documentation
### Overview

The `AsqlDatabase` class represents an Azure SQL Database.

The `AsqlDatabase` class is a subclass of `Notebook`.

### Attributes

#### Required parameters
- **database_name**: The name of the Azure SQL database, required parameter.
- **database_schema**: The schema within the database, required parameter.

#### Optional parameters

--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **database_server**: The server hosting the database
    - constructed based on the environment and data product name
    - e.g. sql-tisc-we-nonprod.database.windows.net:1433
- **linked_service_name**: The name of the linked service for the database.
    - constructed based on the data product name
    - e.g. ls_asql_tisc

### Methods

#### `__init__(database_name: str, database_schema: str) -> AsqlDatabase`

Initializes an `AsqlDatabase` instance.

It sets the `database_name`, `database_schema`, constructs the `database_server` based on the environment and the data product name, and defines the `linked_service_name` based on the data product name.

#### `__eq__(other_database) -> bool`

Checks if two `AsqlDatabase` instances are equal based on their instance type, `database_server`, `database_name`, `database_schema`, and `linked_service_name` attributes.

#### `__str__() -> str`

Returns a string representation of the Azure SQL database linked service.

#### `__repr__() -> str`

Returns a string representation that could be used to recreate the object.

#### `get_token() -> str`

Retrieves the connection string token for the linked service using the TokenLibrary.

#### `build_connection_properties(database_table: str) -> Tuple[dict, str, str]`

Constructs connection properties for a specific database table. It returns a dictionary with connection details, the JDBC URL, and the fully qualified database table name.
```python
connection_properties = {
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "url": "jdbc:sqlserver://databaseserver;databaseName=databasename;      
                    encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30",
            "dbtable": "dbtable",
            "accessToken": "[REDACTED]"
            }
```

### Example Usage

```python
# Create an instance of AsqlDatabase
database = AsqlDatabase("my_database", "my_schema")

# Get the connection token
token = database.get_token()

# Build connection properties for a table
connection_properties, url, dbtable = database.build_connection_properties("my_table")
```
