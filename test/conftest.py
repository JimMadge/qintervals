from os import path
import pytest


@pytest.fixture()
def test_data():
    return path.abspath(path.join(path.dirname(__file__), 'data'))
