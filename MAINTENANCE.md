# `synapse_sdk` — Update List

## High-value
- [ ] **Migrate `setup.py` → `pyproject.toml`** (PEP 621). Modern packaging standard; sends "current stack" signal. `setup.py` is in place as a stepping stone — port `BUILD` / `TEST` extras and metadata over.
- [ ] **Examples folder.** `examples/` with 1-2 worked scenarios (e.g. "convert this local module to a Synapse notebook"). README has inline snippets but no runnable example tree.

## Nice to have

- [ ] **Type hints + mypy in CI.** Even partial coverage helps.
- [ ] **Switch pylint+flake8 → ruff.** Single tool, much faster, modern default.
- [ ] **Pre-commit hooks** (`.pre-commit-config.yaml`).
- [ ] **Status badges** in README: CI, coverage, license, latest release.
- [ ] **LICENSE file** if not already present (MIT or Apache 2.0 typical).
