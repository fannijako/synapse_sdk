#!/bin/bash

set -e

# Variables that needs to be customized for the use case
REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-TISC/_git/lhtdap-tisc-syn"
BRANCH_NAME="fj/ahornboden/modularized_generic"
COMMIT_MESSAGE="automatically commited by commit.sh"

FILES=("generic_utils.py" "vacuum_notebook.py")

# Additional variables
PYTHON_VERSION="python3"
NOTEBOOK_GENERATION_SCRIPT="generate_notebook.py"

# Generated variables
REPOSITORY_NAME=$(basename "$REPOSITORY_URL")
JSON_FILES=("${FILES[@]/.py/.json}")

echo "Virtual environment creation and activation started..."

$PYTHON_VERSION -m venv ".venv"
source .venv/bin/activate

echo "Virtual environment created and activated. Starting the package installations..."

pip install --upgrade pip
pip install -r requirements.txt

echo "Requirements installed for the tests. Starting the pytests..."

pytest test_descriptor.py || exit 1
pytest test_utils.py || exit 1

echo "All tests passed. Deactivating virtual environment..."

deactivate

echo "Virtual environment deactivated. Commiting to the repository..."

git add .
git commit -m $COMMIT_MESSAGE
git push

echo "Git commit is finished for the py files. Starting the .py to .json conversions..."

for file in "${FILES[@]}"; do
    $PYTHON_VERSION $NOTEBOOK_GENERATION_SCRIPT "$file"
done

echo "Finished the .py to .json conversions. Cloning the data product's repository..."

if [ ! -d "$REPOSITORY_NAME" ]; then
    git clone $REPOSITORY_URL
    echo "Data product's repository cloned."
fi
    echo "Data product's repository has already been cloned."

cd $REPOSITORY_NAME

if git show-ref --verify --quiet refs/heads/$BRANCH_NAME; then
    git checkout $BRANCH_NAME
    echo "Local and remote branch already exists. Checked out to the local."
else
    if git ls-remote --exit-code --heads origin $BRANCH_NAME > /dev/null 2>&1; then
        git checkout -b $BRANCH_NAME origin/$BRANCH_NAME
        echo "Remote branch has already existed. Local pair has been created."
    else
        git checkout -b $BRANCH_NAME
        git push --set-upstream origin $BRANCH_NAME
        echo "New local branch has been created and remote branch has been paired."
    fi
fi

cd ..

for file in "${JSON_FILES[@]}"; do
    cp -f notebook/"$file" $REPOSITORY_NAME/notebook/"$file"
done

echo "Generated notebook files have been added to the repository. Starting the commit..."

# TODO: commit to TISC and run integration tests

cd $REPOSITORY_NAME
git add .
git commit -m $COMMIT_MESSAGE
git push

echo "Commit and push finished. Clean-up started."

cd ..
rm -rf $REPOSITORY_NAME
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .venv
rm -rf notebook

clear

echo "Successfully finished."
