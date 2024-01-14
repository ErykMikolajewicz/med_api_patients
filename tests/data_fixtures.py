import json

import pytest

with open('./tests/secrets.json', 'r') as file:
    secrets = json.load(file)


@pytest.fixture(scope="function")
def appointment_data():
    appointment_data = {
        "specialist_id": "9a396a65-16d3-46ac-bd3f-754500f18b91",
        "start": "2024-01-15 14:15",
        "end": "2024-01-15 14:45"
    }

    yield appointment_data
