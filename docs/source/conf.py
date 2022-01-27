# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import datetime
from importlib.metadata import version

# -- Import packages ---------------------------------------------------------

# -- Project information -----------------------------------------------------

project = 'MESMER-OpenSCM Runner'
authors = "Authors, see AUTHORS"
copyright_year = datetime.date.today().year
copyright = "(c) 2021-{} MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich".format(copyright_year)
author = authors

# The full version, including alpha/beta/rc tags
release = version("mesmer_openscmrunner")
# The short X.Y version
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# add sphinx extension modules
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "numpydoc",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

extlinks = {
    "issue": ("https://github.com/mesmer-group/mesmer-openscmrunner/issues/%s", "GH"),
    "pull": ("https://github.com/mesmer-group/mesmer-openscmrunner/pull/%s", "PR"),
}

autosummary_generate = True

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_use_param = False
napoleon_use_rtype = False

# napoleon_use_ivar = True
# napoleon_use_admonition_for_notes = True

numpydoc_class_members_toctree = True
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

html_theme = "sphinx_rtd_theme"
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = []

pygments_style = "sphinx"

# -- Extension configuration -------------------------------------------------

coverage_write_headline = False  # do not write headlines.
