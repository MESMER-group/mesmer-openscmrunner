# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021-2022 MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/
try:
    from importlib.metadata import version as _version
except ImportError:
    # no recourse if the fallback isn't there either...
    from importlib_metadata import version as _version

try:
    __version__ = _version("mesmer_openscmrunner")
except Exception:  # pylint: disable=broad-except
    # Local copy, not installed with setuptools
    __version__ = "unknown"
