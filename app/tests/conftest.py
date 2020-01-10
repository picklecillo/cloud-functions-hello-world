import json
import pytest


@pytest.fixture
def results_from_json():
    def _loader(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    return _loader
