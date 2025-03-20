## Documentation for `Utils` Class
### Overview

The `Utils` class is designed to provide a set of utility methods for various operations such as listing files, handling dates, writing JSON files, and managing delta tables.

### Attributes
- **None**: This class does not have any attributes.

### Methods

#### 1. `__init__`
- **Purpose**: Initializes the `Utils` class.
- **Parameters**: None
- **Returns**: None

#### 2. `__str__`
- **Purpose**: Returns a string representation of the `Utils` class.
- **Parameters**: None
- **Returns**: A string indicating the class name and its methods.

#### 3. `__repr__`
- **Purpose**: Returns a formal string representation of the `Utils` class.
- **Parameters**: None
- **Returns**: A string in the format `Utils()`.

#### 4. `deep_ls`
- **Purpose**: Lists all files and folders in a specified path and its subfolders up to a maximum recursion depth.
- **Parameters**:
  - `path` (str): The path to list.
  - `max_depth` (int, optional): The maximum depth of the listing. Defaults to 1.
- **Returns**: An iterator yielding all files until `max_depth` has been reached.

#### 5. `get_previous_date`
- **Purpose**: Returns the date a specified number of days back from the current date.
- **Parameters**:
  - `days_back` (int): The number of days to go back.
- **Returns**: A string representing the previous date in the format `YYYY-MM-DD`.

#### 6. `write_non_distributed_json`
- **Purpose**: Writes a JSON file to a specified path in ABFSS as a single file, not as a distributed object.
- **Parameters**:
  - `content` (dict): The content to be written to the JSON file.
  - `target_path` (str): The ABFSS path where the file will be written.
- **Returns**: None

#### 7. `get_all_deltas`
- **Purpose**: Creates a dictionary of available delta tables with their paths.
- **Parameters**:
  - `path_list` (list[str]): A list of paths to search for delta tables.
  - `max_depth` (int, optional): The maximum depth to search. Defaults to 3.
- **Returns**: A dictionary where keys are table names and values are dictionaries containing the table URL.

### Example Usage

```python
from datetime import datetime, timedelta
import json
from typing import Iterator

# Initialize the Utils class
utils = Utils()

# List files and folders
for file in utils.deep_ls("/path/to/list", max_depth=2):
    print(file)

# Get previous date
previous_date = Utils.get_previous_date(7)
print(previous_date)

# Write JSON to ABFSS
content = {"key": "value"}
target_path = "abfss://path/to/write.json"
Utils.write_non_distributed_json(content, target_path)

# Get all delta tables
path_list = ["/path/to/search/1", "/path/to/search/2"]
delta_tables = utils.get_all_deltas(path_list)
print(delta_tables)
```

### Notes
- The `deep_ls` method uses `mssparkutils.fs.ls` which is specific to Azure Synapse Analytics environments.
- The `write_non_distributed_json` method writes to a temporary local file before copying it to ABFSS.
- The `get_all_deltas` method searches for `.delta` files within the specified paths and handles `Py4JJavaError` exceptions.
