#!/usr/bin/env bash
#
# Build, test, generate notebook ARM templates, and push them to a data
# product's Azure DevOps repository.
#
# Run with:   bash commit.sh
# (Do NOT `source` this — failures inside it would exit your shell.)

set -euo pipefail

# ---- Customize for your use case --------------------------------------------
REPOSITORY_URL="https://lufthansa-technik@dev.azure.com/lufthansa-technik/LHT-DAP-TISC/_git/lhtdap-tisc-syn"
BRANCH_NAME="fj/ahornboden/modularized_generic"
COMMIT_MESSAGE="automatically committed by commit.sh"

# Python files to convert to Synapse notebook templates (paths from repo root).
FILES=(
    "src/generic_utils.py"
    "src/vacuum_notebook.py"
    "tests/test_helper.py"
    "tests/test_asql_database.py"
    "tests/test_azureml.py"
    "tests/test_data_product.py"
    "tests/test_keyvault.py"
    "tests/test_kusto.py"
    "tests/test_synstorage.py"
    "tests/test_utils.py"
    "tests/test_notebook.py"
    "tests/test_dataframe.py"
    "tests/test_table.py"
    "tests/test_generic_notebook.py"
)

# ---- Constants --------------------------------------------------------------
PYTHON="${PYTHON:-python3}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
NOTEBOOK_DIR="${REPO_ROOT}/notebook"
GENERATE_SCRIPT="${REPO_ROOT}/src/generate_notebook.py"
REPOSITORY_NAME="$(basename "$REPOSITORY_URL")"

# ---- Build, test, lint ------------------------------------------------------
echo ">> Creating virtual environment..."
"$PYTHON" -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo ">> Installing dependencies (make build-all)..."
make build-all

echo ">> Running tests (make test)..."
make test

echo ">> Running linter (make lint)..."
make lint

deactivate

# ---- Commit source changes to this repo, if any -----------------------------
echo ">> Staging source changes..."
git add src tests
if git diff --cached --quiet; then
    echo "   No source changes to commit."
else
    git commit -m "$COMMIT_MESSAGE"
    git push
fi

# ---- Generate notebook ARM templates ----------------------------------------
echo ">> Generating notebook ARM templates..."
mkdir -p "$NOTEBOOK_DIR"
for file in "${FILES[@]}"; do
    src_dir="$(dirname "$file")"
    base="$(basename "$file")"
    # generate_notebook.py reads input relative to cwd; run from the source
    # directory so it picks up the right file and writes a flat output name.
    ( cd "${REPO_ROOT}/${src_dir}" && "$PYTHON" "$GENERATE_SCRIPT" "$base" "$NOTEBOOK_DIR" )
done

# ---- Clone (or reuse) the target repository ---------------------------------
if [ ! -d "$REPOSITORY_NAME" ]; then
    echo ">> Cloning target repository..."
    git clone "$REPOSITORY_URL"
else
    echo ">> Target repository already present, reusing local clone."
fi

# ---- Check out the target branch --------------------------------------------
(
    cd "$REPOSITORY_NAME"
    if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
        git checkout "$BRANCH_NAME"
    elif git ls-remote --exit-code --heads origin "$BRANCH_NAME" >/dev/null 2>&1; then
        git checkout -b "$BRANCH_NAME" "origin/${BRANCH_NAME}"
    else
        git checkout -b "$BRANCH_NAME"
        git push --set-upstream origin "$BRANCH_NAME"
    fi
)

# ---- Copy generated templates into the target repo --------------------------
mkdir -p "${REPOSITORY_NAME}/notebook"
for file in "${FILES[@]}"; do
    json="$(basename "${file%.py}.json")"
    cp -f "${NOTEBOOK_DIR}/${json}" "${REPOSITORY_NAME}/notebook/${json}"
done

# ---- Commit + push to target repo -------------------------------------------
(
    cd "$REPOSITORY_NAME"
    git add notebook
    if git diff --cached --quiet; then
        echo ">> No notebook changes to push."
    else
        git commit -m "$COMMIT_MESSAGE"
        git push
        echo ">> Pushed notebook updates to ${BRANCH_NAME}."
    fi
)

# ---- Clean up ---------------------------------------------------------------
echo ">> Cleaning up..."
rm -rf "$REPOSITORY_NAME" .venv .pytest_cache "$NOTEBOOK_DIR"
find . -type d -name __pycache__ -prune -exec rm -rf {} +

echo ">> Done."
