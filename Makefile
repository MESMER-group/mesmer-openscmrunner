.DEFAULT_GOAL := help

OS=`uname`
SHELL=/bin/bash

CONDA_ENV_YML=environment.yml

N_JOBS ?= 1

ifndef CONDA_PREFIX
$(error Conda environment not active. Activate your conda environment before using this Makefile.)
else
ifeq ($(CONDA_DEFAULT_ENV),base)
$(error Do not install to conda base environment. Activate a different conda environment and rerun make. A new environment can be created with e.g. `conda create --name mesmer-openscmrunner`))
endif
VENV_DIR=$(CONDA_PREFIX)
endif

# use mamba if available
MAMBA_EXE := $(shell command -v mamba 2> /dev/null)
ifndef MAMBA_EXE
MAMBA_OR_CONDA=$(CONDA_EXE)
else
MAMBA_OR_CONDA=$(MAMBA_EXE)
endif

PYTHON=$(VENV_DIR)/bin/python

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: format
format:  ## re-format files
	make isort
	make black

.PHONY: docs
black: $(VENV_DIR)  ## apply black formatter to source and tests
	@status=$$(git status --porcelain src tests docs scripts); \
	if test ${FORCE} || test "x$${status}" = x; then \
		$(VENV_DIR)/bin/black --exclude _version.py src setup.py tests docs/source/conf.py; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

.PHONY: isort
isort: $(VENV_DIR)  ## format the code
	@status=$$(git status --porcelain src tests); \
	if test ${FORCE} || test "x$${status}" = x; then \
		$(VENV_DIR)/bin/isort src setup.py tests; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

.PHONY: docs
docs: $(VENV_DIR)  ## build the docs
	$(VENV_DIR)/bin/sphinx-build -M html docs/source docs/build

.PHONY: test
test: $(VENV_DIR)  ## run the testsuite
	$(VENV_DIR)/bin/pytest -r a -v --cov=mesmer_openscmrunner  --cov-report term-missing

.PHONY: test_cov_xml
test_cov_xml: $(VENV_DIR)  ## run the testsuite with xml report for codecov
	$(VENV_DIR)/bin/pytest -r a -v --cov=mesmer_openscmrunner --cov-report xml

test-install: $(VENV_DIR)  ## test whether installing locally in a fresh env works
	$(eval TEMPVENV := $(shell mktemp -d))
	python3 -m venv $(TEMPVENV)
	$(TEMPVENV)/bin/pip install wheel pip --upgrade
	$(TEMPVENV)/bin/pip install .
	$(TEMPVENV)/bin/python scripts/test-install.py

.PHONY: conda-environment
conda-environment:  $(VENV_DIR) ## make virtual environment for development
$(VENV_DIR): $(CONDA_ENV_YML) setup.py setup.cfg pyproject.toml
	$(MAMBA_OR_CONDA) config --add channels conda-forge
	$(MAMBA_OR_CONDA) install -y --file $(CONDA_ENV_YML)
	# Install the remainder of the dependencies using pip
	$(VENV_DIR)/bin/pip install --upgrade pip wheel
	$(VENV_DIR)/bin/pip install -e .[dev]
	touch $(VENV_DIR)
