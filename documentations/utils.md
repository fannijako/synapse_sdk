## Documentation for `Utils` Class
### Overview

The `Utils` class is designed to provide a set of utility methods for various operations such as listing files, handling dates, writing JSON files, and managing delta tables.

The `Utils` class serves as the mother class for all other modules.

### Attributes
--

### Methods
#### `__str__() -> str`
Returns a string representation of Utils.

#### `__repr__() -> str`
Returns a string representation that could be used to recreate the object.

#### `deep_ls(path: str, max_depth: int = 1) -> Iterator[str]:`
Lists all files and folders in a specified path and its subfolders up to a maximum recursion depth.

- **Parameters**:
  - `path` (str): The abfss path to list.
  - `max_depth` (int, optional): The maximum depth of the listing. Defaults to 1.

- **Returns**: An iterator yielding all files until `max_depth` has been reached.

#### `get_previous_date(days_back: int) -> str:`
Returns the date a specified number of days back from the current date.

- **Parameters**:
  - `days_back` (int): The number of days to go back.
- **Returns**: A string representing the previous date in the format `YYYY-MM-DD`.

#### `write_non_distributed_json(content: dict, target_path: str) -> None:`
Writes a JSON file to a specified path in ABFSS as a single file, not as a distributed object.

- **Parameters**:
  - `content` (dict): The content to be written to the JSON file.
  - `target_path` (str): The abfss path where the file will be written.

#### `get_all_deltas(path_list: list[str], max_depth: int = 3) -> dict:`
Creates a dictionary of available delta tables with their paths.

- **Parameters**:
  - `path_list` (list[str]): A list of paths to search for delta tables.
  - `max_depth` (int, optional): The maximum depth to search. Defaults to 3.
- **Returns**: A dictionary where keys are table names and values are dictionaries containing the table URL.

### Example Usage

```python
utils = Utils()

for file in utils.deep_ls("/path/to/list", max_depth=2):
    print(file)

previous_date = Utils.get_previous_date(7)
print(previous_date)

Utils.write_non_distributed_json({"key": "value"},  "abfss://path/to/write.json")

path_list = ["/path/to/search/1", "/path/to/search/2"]
delta_tables = utils.get_all_deltas(path_list)
print(delta_tables)
```

### Notes
- The module uses `mssparkutils.fs` which is specific to Azure Synapse Analytics environments.
- The `write_non_distributed_json` method writes to a temporary local file before copying it to abfss.
