.. installation:

Installation
============

Installing with conda
---------------------

MESMER-OpenSCM Runner is not yet installabale via conda.
However, given that many of its dependencies are not pure Python, we recommend using a conda environment nonetheless (and installing MESMER-OpenSCM Runner via pip as a final step).
The easiest way to install scmdata is using conda, either using the full
`Anaconda <https://docs.continuum.io/anaconda/>`_ distribution which includes a collection of
popular data science packages or the smaller
`Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ distribution. Using conda
is the recommended method for installing scmdata for most users.

.. code:: bash

    # install key dependencies via conda
    conda install -c conda-forge mesmer pip
    # at present, MESMER-OpenSCM Runner is only installable via pip
    pip install mesmer-openscmrunner

Installing with pip
-------------------

MESMER-OpenSCM can be installed from `PyPi <https://pypi.org/>`_ using pip.

We recommend creating a virtual environment to manage this and any other libraries your
project requires.

.. code:: bash

    pip install mesmer-openscmrunner
