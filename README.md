# synapse_sdk
Synapse SDK

## Generate Synapse notebook from a py file
You can create a Synapse notebook's ARM template, which needs to be committed to Azure DevOps from the py source file using the generate_notebook.py file.

```
python3 generate_notebook.py
```

Follow the input instructions in the terminal to specify which file you would like to convert and to specify where to place the generated json.

## Commit the generated Synapse notebook ARM template to Azure DevOps

Run the shell script to generate the notebook template and commit to a data product's Azure DevOps repository.

Customize the variables in the commit.sh

- TEST_FILES=("generic_utils.py" "test_descriptor.py" "test_notebook.py" "test_utils.py" "vacuum_notebook.py")
    - py files to convert to notebook and commit
- REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-TISC/_git/lhtdap-tisc-syn"
    - repository url to commit to
- BRANCH_NAME="fj/ahornboden/modularized_generic"
    - branch name within the repository (either existing or non-existing)
- COMMIT_MESSAGE="automatically commited by commit.sh"
    - commit message to use

Run the script:

```
source ./commit.sh
```

## Generic_utils

The generic_utils.py file contains all the classes that you'll need in your data product. Generate a Synapse notebook from this file and commit to Azure DevOps to use it within the data product.

## Tests
The following files are testing the utilities. Run

```
pytest
```

to test them all before merge.

### Vacuum_notebook.py
Runs VACUUM command on all tables in the data product's storage account. Use the generate_notebook.py to convert it to Synapse notebook and commit.
