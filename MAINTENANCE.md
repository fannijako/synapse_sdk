# `synapse_sdk` — Update List

## Done (maintenance branch)

- [x] **Repo layout.** Moved source modules to `src/` and tests to `tests/` (was: flat root with `*.py` and `test_*.py` interleaved).
- [x] **Packaging.** Replaced `requirements.txt` with `setup.py` declaring `name`, `version=0.1.0`, `python_requires>=3.10`, and `extras_require` for `build` / `test`.
- [x] **Pin dependency versions.** Lower + upper bounds on test deps (`pytest`, `pytest-cov`, `pylint`, `flake8`) in `setup.py`.
- [x] **Makefile.** `venv` / `build` / `build-test` / `lint` / `test` / `clean` targets so contributors have a one-command workflow.
- [x] **Lint config.** `.pylintrc` checked in (was: ad-hoc CLI flags only).
- [x] **CI workflow.** `.github/workflows/linter.yml` runs `make build-all`, flake8, pylint, and pytest on push/PR to `main`.

## Critical

- [ ] **README rewrite.** Expand to cover:
  - Problem statement: why bridging local Python ↔ Synapse notebooks matters (the exact "notebooks that kind of work" pain RevoData mentions)
  - Architecture: 2-3 sentences + a simple diagram (mermaid is fine)
  - Decision log: why ARM template generation vs alternatives, why Azure DevOps integration, why these utility classes
  - Usage examples: at least one end-to-end snippet
  - Limitations: what it doesn't do (sets reader expectations)
  - Reference the new `src/` + `tests/` layout and the `make` targets
- [ ] **Extend CI** (`.github/workflows/linter.yml`):
  - Rename to `ci.yml` — it runs tests too, not just lint
  - Add a Python 3.10 + 3.11 matrix (currently 3.10 only)
  - Surface pytest coverage (already wired in `make test`)
- [ ] **Tag a release.** 190 commits with zero releases looks abandoned. Tag `v0.1.0` (already set in `setup.py`) with a CHANGELOG entry.

## High-value

- [ ] **Migrate `setup.py` → `pyproject.toml`** (PEP 621). Modern packaging standard; sends "current stack" signal. `setup.py` is in place as a stepping stone — port `BUILD` / `TEST` extras and metadata over.
- [ ] **Add CHANGELOG.md.** Even a brief one. Demonstrates release discipline. First entry should cover the maintenance-branch restructuring.
- [ ] **Document the Python→notebook conversion model.** Architecture doc or expanded README section — what gets converted, what doesn't, how cell boundaries are handled, how dependencies resolve.
- [ ] **Examples folder.** `examples/` with 1-2 worked scenarios (e.g. "convert this local module to a Synapse notebook").

## Nice to have

- [ ] **Type hints + mypy in CI.** Even partial coverage helps.
- [ ] **Switch pylint+flake8 → ruff.** Single tool, much faster, modern default.
- [ ] **Pre-commit hooks** (`.pre-commit-config.yaml`).
- [ ] **Status badges** in README: CI, coverage, license, latest release.
- [ ] **LICENSE file** if not already present (MIT or Apache 2.0 typical).
