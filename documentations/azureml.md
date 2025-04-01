## AzureMachineLearningWorkspace Class Documentation
### Overview

The `AzureMachineLearningWorkspace` class represents an Azure Machine Learning Workspace.

The `AzureMachineLearningWorkspace` class is a subclass of `Notebook`.

### Attributes

#### Required parameters

--

#### Optional parameters

--

#### Inherited attributes
- All attributes of a Notebook class, see in `notebook.md`.

#### Additional attributes
- **`linked_service_name`**: the name of the linked service for the Azure ML Workspace.
    - constructed based on the data product name and version
    - e.g. mlwtisc002

### Methods

#### `__init__() -> AzureMachineLearningWorkspace`
Initializes an instance of `AzureMachineLearningWorkspace`.

It sets the `linked_service_name` attribute based on the data product name and version.

#### `__eq__(other_azureml: AzureMachineLearningWorkspace) -> bool`
Checks if two instances of `AzureMachineLearningWorkspace` are equal. Equality is determined by both instances being of the same type and having the same `linked_service_name`.

#### `__str__(): -> str`
Returns a string representation of the `AzureMachineLearningWorkspace` instance, including the linked service name.

#### `__repr__(): -> str`
Returns a string that represents the type of the instance.

### Example Usage

```python
workspace = AzureMachineLearningWorkspace()

# Get the linked service's name
print(workspace.linked_service_name)
```
