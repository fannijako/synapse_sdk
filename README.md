# Synapse utilities

Utility scripts to help create a software engineering like development in a Synapse Analytics workspace.

## Generate Synapse notebook ARM template from a py file
You can create a Synapse notebook's ARM template from a .py file using this script. 

**Arguments**:
1. the name of the .py file to convert (Defaults to generic_utils.py)
1. the folder to put the result in (Defaults to notebook)

See the next section for a script to commit the generated files to Azure DevOps.

The result of the following script
```
python3 generate_notebook.py generic_utils.py notebook
```
is a notebook ARM template within the notebook subfolder, where the code lines are the same as in the generic_utils.py.

## Generate Synapse notebook from a py file, test them and commit the generated Synapse notebook ARM template to Azure DevOps

Run the following shell script to generate the notebook template and commit to a data product's Azure DevOps repository.

Customize the variables in the commit.sh:

- FILES: py files to convert to notebook and commit
- REPOSITORY_URL: repository url to commit to
- BRANCH_NAME: branch name within the repository (either existing or non-existing)
- COMMIT_MESSAGE: commit message to use

Run the script:

```
source ./commit.sh
```

Keep in mind that before the first run you need set the parameter values and make the file executable and during the first commit to a new repository, you'll need to provide credentials.

#### Steps of the shell script

1. Set parameter values (see above)
1. Create and activate a virtual environment
1. Install dependencies
1. Run pytest
1. Deactivate virtual environment
1. Convert the .py files to .json ARM templates within the notebooks subfolder
1. Clone the data product's repository
1. Checkout to the specified branch
1. Copy the .json files to the notebook folder within the Synapse structure
1. Commit and push the changes to Azure DevOps
1. Clean-up (remove cloned repository and not needed directories)

## Generic_utils

The generic_utils.py file contains all the commonly used scripts in Synapse in a modularized form. 

To use it in your data product, generate a Synapse notebook from this file and commit to Azure DevOps. For steps, see the sections above.

#### Classes

1. Utils
1. Notebook
1. DataProduct
1. Table
1. DataFrame
1. KeyVault
1. aSQLDataBase

## Tests
The following files are testing the utilities:

- test_descriptor.py
- test_utils.py
- test_notebook.py

Run

```
pytest
```

to test them all before you make a commit. The shell script only lets you make a commit to Azure DevOps, if all tests have been passed.

## Vacuum_notebook.py

An example file to use the modularized utilities within a Synapse Analytics workspace. 

It runs VACUUM command on all tables in the data product's storage account. 

Use the shell script to convert it to Synapse notebook and to commit it to Azure DevOps.
