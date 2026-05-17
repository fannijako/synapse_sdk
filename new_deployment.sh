#!/usr/bin/env bash
#
# Copy the latest generic_utils notebook from the tisc repo into another data
# product's repo and open a deployment branch with the change.
#
# Run with:   bash new_deployment.sh

set -euo pipefail

# ---- Customize --------------------------------------------------------------
TARGET_DATA_PRODUCT_NAME="CTT"

# ---- Constants --------------------------------------------------------------
PYTHON="${PYTHON:-python3}"
JSON_FILES=("generic_utils.json")
COMMIT_MESSAGE="generic_utils notebook automatically committed by new_deployment.sh"

TISC_REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-TISC/_git/lhtdap-tisc-syn"
TISC_REPOSITORY_NAME="$(basename "$TISC_REPOSITORY_URL")"

TARGET_REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-${TARGET_DATA_PRODUCT_NAME}/_git/lhtdap-${TARGET_DATA_PRODUCT_NAME}-syn"
TARGET_REPOSITORY_NAME="$(basename "$TARGET_REPOSITORY_URL")"

CURRENT_DATE="$(date +%Y-%m-%d)"
BRANCH_NAME="automation/generic_utils_deployment/${CURRENT_DATE}"

# ---- Helpers ----------------------------------------------------------------
clone_or_update() {
    local url="$1"
    local name="$2"

    if [ ! -d "$name" ]; then
        echo ">> Cloning ${name}..."
        git clone "$url"
    else
        echo ">> ${name} already cloned, pulling latest main..."
    fi

    (
        cd "$name"
        git checkout main
        git pull --ff-only
    )
}

# ---- Workflow ---------------------------------------------------------------
clone_or_update "$TISC_REPOSITORY_URL" "$TISC_REPOSITORY_NAME"
clone_or_update "$TARGET_REPOSITORY_URL" "$TARGET_REPOSITORY_NAME"

echo ">> Preparing deployment branch ${BRANCH_NAME} in ${TARGET_REPOSITORY_NAME}..."
(
    cd "$TARGET_REPOSITORY_NAME"
    if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
        git checkout "$BRANCH_NAME"
    elif git ls-remote --exit-code --heads origin "$BRANCH_NAME" >/dev/null 2>&1; then
        git checkout -b "$BRANCH_NAME" "origin/${BRANCH_NAME}"
    else
        git checkout -b "$BRANCH_NAME"
        git push --set-upstream origin "$BRANCH_NAME"
    fi
)

echo ">> Copying notebook templates..."
mkdir -p "${TARGET_REPOSITORY_NAME}/notebook"
for file in "${JSON_FILES[@]}"; do
    cp -f "${TISC_REPOSITORY_NAME}/notebook/${file}" "${TARGET_REPOSITORY_NAME}/notebook/${file}"
done

echo ">> Committing + pushing changes..."
(
    cd "$TARGET_REPOSITORY_NAME"
    git add notebook
    if git diff --cached --quiet; then
        echo ">> No notebook changes to push."
    else
        git commit -m "$COMMIT_MESSAGE"
        git push
        echo ">> Pushed deployment to ${BRANCH_NAME}."
    fi
)

echo ">> Cleaning up..."
rm -rf "$TARGET_REPOSITORY_NAME" "$TISC_REPOSITORY_NAME"

echo ">> Done."
