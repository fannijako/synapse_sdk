# Changelog

All notable changes to `synapse_sdk` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-17

First tagged release. The maintenance branch reshaped the repo from a flat
script-style layout into an installable package with structured tests and CI.

### Added
- `src/` package layout (`generic_utils`, `generate_notebook`,
  `notebook_converter`, `vacuum_notebook`) installable via `pip install -e .`.
- `tests/` package with all test modules restructured into pytest classes —
  one `test_*` method per assertion, `try/except`-then-`AssertionError`
  idioms converted to `pytest.raises`.
- `setup.py` with `build` and `test` extras (delta-spark, pyspark, pytest,
  pytest-cov, pylint, flake8).
- `Makefile` targets: `venv`, `build`, `build-test`, `build-all`, `lint`,
  `test`, `run`, `clean`.
- `.github/workflows/ci.yml` running lint and tests on push.
- `MAINTENANCE.md` tracking outstanding modernization work.
- `CHANGELOG.md` (this file).

### Changed
- Imports rewritten from notebook-style (`from generic_utils import X`) to
  package-qualified (`from src.generic_utils import X`,
  `from tests.test_helper import X`).
- Pylint configuration in `.pylintrc` — disabled `redefined-outer-name` and
  `too-few-public-methods` to accommodate pytest fixture and test-class
  idioms; added per-class disables for known false positives in
  `generic_utils.py` (descriptor `_name`, lazy-init attributes on `Table`,
  `too-many-public-methods` on `Notebook`).
- `delta-spark` constraint downgraded from `>=4.0,<5.0` to `>=3.0,<4.0` to
  match the pinned `pyspark>=3.5,<4.0`.
- README rewritten with installation, usage, and contribution sections.

### Removed
- Top-level `requirements.txt` (replaced by `extras_require` in `setup.py`).

[0.1.0]: https://github.com/fannijako/synapse_sdk/releases/tag/v0.1.0
