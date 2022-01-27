# MESMER-OpenSCM Runner, land-climate dynamics group, S.I. Seneviratne
# Copyright (c) 2021-2022 MESMER-OpenSCM Runner contributors, listed in AUTHORS, and ETH Zurich.
# Licensed under the GNU General Public License v3.0 or later; see LICENSE or https://www.gnu.org/licenses/

import os.path

import pytest

REPO_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEST_DATA_DIR = os.path.join(REPO_ROOT_DIR, "tests", "test-data")


@pytest.fixture
def test_data_dir():
    return TEST_DATA_DIR


@pytest.fixture
def repo_root_dir():
    return REPO_ROOT_DIR


def pytest_addoption(parser):
    parser.addoption(
        "--update-copyright-notices",
        action="store_true",
        default=False,
        help="Overwrite expected values",
    )


@pytest.fixture
def update_copyright_notices(request):
    return request.config.getoption("--update-copyright-notices")
