import os.path

import pytest

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test-data")


@pytest.fixture
def test_data_dir():
    return TEST_DATA_DIR
