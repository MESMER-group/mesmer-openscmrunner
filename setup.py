from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

import versioneer

PACKAGE_NAME = "mesmer-openscmrunner"
DESCRIPTION = "Coupling between MESMER and OpenSCM-Runner"
KEYWORDS = [
    "MESMER",
    "netCDF",
    "python",
    "climate",
    "atmosphere",
    "simple climate model",
    "reduced complexity climate model",
    "emulation",
    "earth system model emulation",
]

AUTHORS = [
    ("Zeb Nicholls", "zebedee.nicholls@climate-energy-college.org"),
    ("Lea Beusch", "lea.beusch@env.ethz.ch"),
    ("Mathias Hauser", "mathias.hauser@env.ethz.ch"),
]
URL = "https://github.com/MESMER-group/mesmer-openscmrunner"
PROJECT_URLS = {
    "Bug Reports": "https://github.com/MESMER-group/mesmer-openscmrunner/issues",
    # "Documentation": "https://mesmer-openscmruner.readthedocs.io/en/latest",
    "Source": "https://github.com/MESMER-group/mesmer-openscmrunner",
}
LICENSE = "GPLv3+"  # I think this is the right short-hand...
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

REQUIREMENTS = [
    # "mesmer",  # once released
    "openscm-runner>=0.6",
    "scmdata>=0.9,<0.10",  # whilst running notebooks with rcmip phase 2 output
    "xarray==0.17.0",  # whilst running notebooks with rcmip phase 2 output
]
REQUIREMENTS_TESTS = [
    "codecov",
    "nbval",
    "pytest",
    "pytest-cov",
    "pytest-xdist",
]
REQUIREMENTS_NOTEBOOKS = [
    "ipywidgets",
    "notebook",
    "seaborn",
]
REQUIREMENTS_DOCS = [
    "nbsphinx",
    "sphinx",
    "sphinx_rtd_theme",
    "sphinx-copybutton",
]
REQUIREMENTS_DEPLOY = ["twine>=1.11.0", "setuptools>=38.6.0", "wheel>=0.31.0"]
requirements_dev = [
    *[
        "bandit",
        "black",
        "black-nb",
        "flake8",
        "isort",
        "mypy",
        "nbdime",
        "openscm-zenodo",
        "pydocstyle",
        "pylint",
    ],
    *REQUIREMENTS_DEPLOY,
    *REQUIREMENTS_DOCS,
    *REQUIREMENTS_NOTEBOOKS,
    *REQUIREMENTS_TESTS,
]

REQUIREMENTS_EXTRAS = {
    "deploy": REQUIREMENTS_DEPLOY,
    "dev": requirements_dev,
    "docs": REQUIREMENTS_DOCS,
    "notebooks": REQUIREMENTS_NOTEBOOKS,
    "tests": REQUIREMENTS_TESTS,
}

SOURCE_DIR = "src"

# no tests/docs in `src` so don't need exclude
PACKAGES = find_packages(SOURCE_DIR)
PACKAGE_DIR = {"": SOURCE_DIR}
PACKAGE_DATA = {}

README = "README.rst"

with open(README, "r") as readme_file:
    README_TEXT = readme_file.read()


class MesmerOpenSCMRunner(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        pytest.main(self.test_args)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({"test": MesmerOpenSCMRunner})

setup(
    name=PACKAGE_NAME,
    version=versioneer.get_version(),
    description=DESCRIPTION,
    long_description=README_TEXT,
    long_description_content_type="text/x-rst",
    author=", ".join([author[0] for author in AUTHORS]),
    author_email=", ".join([author[1] for author in AUTHORS]),
    url=URL,
    project_urls=PROJECT_URLS,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require=REQUIREMENTS_EXTRAS,
    cmdclass=cmdclass,
)
