from typing import Any
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.domain.models.appointments import AppointmentCreate


@pytest.fixture(scope="function")
def appointment_data(request):
    correct_data = {
        'specialist_id': uuid4(),
        'start': '2024-12-12T08:15',
        'end': '2024-12-12T08:30',
        'patient_id': uuid4()
    }
    return correct_data


def test_correct_data(appointment_data: dict[str, Any]):
    AppointmentCreate.model_validate(appointment_data)


@pytest.mark.parametrize('patient_id', [str(uuid4()) + '4', str(uuid4())[-1:], 'string test', None])
def test_invalid_patient_id(patient_id, appointment_data: dict[str, Any]):
    appointment_data['patient_id'] = patient_id
    with pytest.raises(ValidationError):
        AppointmentCreate.model_validate(appointment_data)


@pytest.mark.parametrize('doctor_id', ['39bf0d1b8-e9ed-4306-ba93-a513911741c3',
                                       '9bf-0d1b8e9ed-4306-ba93-a513911741c3',
                                       '9bf-0d1b8-e9ed-4306-ba93-a513911741c3'])
def test_invalid_doctor_id(doctor_id, appointment_data: dict[str, Any]):
    appointment_data['patient_id'] = doctor_id
    with pytest.raises(ValidationError):
        AppointmentCreate.model_validate(appointment_data)


@pytest.mark.parametrize('start', ['2023-12-15', '112-15-06T12:40'])
def test_invalid_start_date(start, appointment_data: dict[str, Any]):
    appointment_data['start'] = start
    with pytest.raises(ValidationError):
        AppointmentCreate.model_validate(appointment_data)


@pytest.mark.parametrize('end', [None, '15-12-2023T8:15'])
def test_invalid_end_date(end, appointment_data: dict[str, Any]):
    appointment_data['end'] = end
    with pytest.raises(ValidationError):
        AppointmentCreate.model_validate(appointment_data)
