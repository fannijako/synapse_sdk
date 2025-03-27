#!/bin/bash

# Customizable variables
TARGET_DATA_PRODUCT_NAME="CTT"

# Additional variables
PYTHON_VERSION="python3"
BRANCH_NAME="automation/generic_utils_deployment"
COMMIT_MESSAGE="generic_utils notebook automatically commited by new_deployment.sh"
JSON_FILES=("generic_utils.json")

# Generated variables
TISC_REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-TISC/_git/lhtdap-tisc-syn"
TISC_REPOSITORY_NAME=$(basename "$TISC_REPOSITORY_URL")

TARGET_REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-${TARGET_DATA_PRODUCT_NAME}/_git/lhtdap-${TARGET_DATA_PRODUCT_NAME}-syn"
TARGET_REPOSITORY_NAME=$(basename "$TARGET_REPOSITORY_URL")

CURRENT_DATE=$(date +%Y-%m-%d)
BRANCH_NAME="${BRANCH_NAME}/${CURRENT_DATE}"

# Workflow
echo "Cloning tisc's repository..."
if [ ! -d "$TISC_REPOSITORY_NAME" ]; then
    git clone $TISC_REPOSITORY_URL
    echo "Tisc's repository cloned."
    git checkout main
fi
    echo "Tisc's repository has already been cloned. Pulling latest version."

    cd $TISC_REPOSITORY_NAME
    git checkout main
    git pull
    cd ..

echo "Cloning the data product's repository..."

if [ ! -d "$TARGET_REPOSITORY_NAME" ]; then
    git clone $TARGET_REPOSITORY_URL
    echo "Data product's repository cloned."
fi
    echo "Data product's repository has already been cloned. Pulling latest version."
    cd $TARGET_REPOSITORY_NAME
    git checkout main
    git pull
    cd ..

echo "Checkout to new branch in the data product's repository."

cd $TARGET_REPOSITORY_NAME

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
    cp -f $TISC_REPOSITORY_NAME/notebook/"$file" $TARGET_REPOSITORY_NAME/notebook/"$file"
done

echo "Generated notebook files have been added to the repository. Starting the commit..."

cd $TARGET_REPOSITORY_NAME
git add .
git commit -m $COMMIT_MESSAGE
git push

echo "Commit and push finished. Clean-up started."

cd ..
rm -rf $TARGET_REPOSITORY_NAME
rm -rf $TISC_REPOSITORY_NAME

echo "Successfully finished."
