.DEFAULT_GOAL := help

OS=`uname`
SHELL=/bin/bash

CONDA_ENV_YML=environment.yml

FILES_TO_FORMAT_PYTHON=setup.py examples src tests

N_JOBS ?= 1

ifndef CONDA_PREFIX
$(error Conda environment not active. Activate your conda environment before using this Makefile.)
else
ifeq ($(CONDA_DEFAULT_ENV),base)
$(error Do not install to conda base environment. Activate a different conda environment and rerun make. A new environment can be created with e.g. `conda create --name mesmer-openscmrunner`))
endif
VENV_DIR=$(CONDA_PREFIX)
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

# TODO: add docs/source/conf.py  back in here
black: $(VENV_DIR)  ## apply black formatter to source and tests
	@status=$$(git status --porcelain src tests docs scripts); \
	if test ${FORCE} || test "x$${status}" = x; then \
		$(VENV_DIR)/bin/black --exclude _version.py setup.py src tests; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

isort: $(VENV_DIR)  ## format the code
	@status=$$(git status --porcelain src tests); \
	if test ${FORCE} || test "x$${status}" = x; then \
		$(VENV_DIR)/bin/isort src tests setup.py; \
	else \
		echo Not trying any formatting. Working directory is dirty ... >&2; \
	fi;

.PHONY: test
test: $(VENV_DIR)  ## run the testsuite
	$(VENV_DIR)/bin/pytest --cov -r a -v --cov-report term-missing

.PHONY: conda-environment
conda-environment:  $(VENV_DIR) mesmer-environment.yml  ## make virtual environment for development
$(VENV_DIR): $(CONDA_ENV_YML) setup.py
	$(CONDA_EXE) config --add channels conda-forge
	$(CONDA_EXE) install -y --file $(CONDA_ENV_YML)
	# can remove once mesmer is conda installable
	$(CONDA_EXE) install -y --file mesmer-environment.yml
	# Install the remainder of the dependencies using pip
	$(VENV_DIR)/bin/pip install --upgrade pip wheel
	$(VENV_DIR)/bin/pip install -e .[dev]
	$(VENV_DIR)/bin/jupyter nbextension enable --py widgetsnbextension
	touch $(VENV_DIR)
