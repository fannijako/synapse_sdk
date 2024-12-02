# Synapse SDK

## How to use the library?

### Notebook converter

The notebook converter is intended to create py files from the json ARM templates of the Synapse notebooks, so that it can be source controlled in its general meaning and IDEs can be used during development.

Place the content of the Synapse Azure DevOps repository to the folder and execute the following command:

```bash
python notebook_converter.py
```

The .py files will be added to the notebook_py folder.

Neither the notebook nor the notebook_py folder is source controlled.
