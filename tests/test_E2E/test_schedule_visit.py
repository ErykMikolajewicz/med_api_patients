import httpx
import pytest
from fastapi import status

from tests.data_fixtures import secrets, appointment_data


@pytest.fixture(autouse=True, scope='module')
def patient_token(log_as):
    patient_login = secrets['patient_login']
    patient_password = secrets['patient_password']
    login_data = log_as(patient_login, patient_password)
    patient_token = login_data['access_token']
    yield patient_token


def test_try_add_visit_without_token(appointment_data, test_client: httpx.Client):
    response = test_client.post(f"/appointments", json=appointment_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_visit(patient_token, appointment_data, test_client: httpx.Client):
    response = test_client.post(f"/appointments", json=appointment_data,
                                headers={'Authorization': 'Bearer ' + patient_token})
    assert response.status_code == status.HTTP_201_CREATED

