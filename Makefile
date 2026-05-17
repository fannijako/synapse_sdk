.PHONY: venv build build-test build-all lint test commit deploy clean
PYFILES = $(shell git ls-files '*.py')
LOCAL_TESTS = tests/test_asql_database.py tests/test_azureml.py tests/test_descriptor.py tests/test_keyvault.py tests/test_kusto.py tests/test_notebook.py tests/test_synstorage.py tests/test_utils.py tests/test_utils_local.py

venv:
	python -m venv .venv

build:
	pip install --upgrade pip
	pip install setuptools
	pip install -e .[build]

build-test: build
	pip install -e .[test]

build-all: build build-test

lint:
	pylint $(PYFILES) --disable=R0801,W0511,R0401
	flake8 $(PYFILES) --count --exit-zero --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv
	flake8 $(PYFILES) --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=.venv

test: build-all
	python -m pytest $(LOCAL_TESTS)
	python -m pytest $(LOCAL_TESTS) --cov=src --cov-report=term-missing --cov-report=xml

commit:
	bash commit.sh

deploy:
	bash new_deployment.sh

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
