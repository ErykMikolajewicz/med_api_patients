from datetime import datetime, date

from fastapi import HTTPException, status

import src.repositories.appointments as repo_appoint
import src.repositories.specialists as repo_working_time
from src.domain.services.appointment_scheduling import validate_specialist_working_time


async def add_appointment(session, appointment):
    specialist_id = appointment['specialist_id']
    visit_date: datetime = appointment['start']
    visit_date: date = visit_date.date()

    working_time_data_access = repo_working_time.Specialists(session)
    doctor_working_time = await working_time_data_access.get_working_time(specialist_id, visit_date)

    is_valid_visit_time = await validate_specialist_working_time(appointment, doctor_working_time)
    if not is_valid_visit_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Chosen visit date is not available')

    appointment_data_access = repo_appoint.Appointments(session)
    new_appointment = await appointment_data_access.add(appointment)
    return new_appointment


async def get_appointments_list(session, patient_id, appointments_from, appointments_to):
    appointment_data_access = repo_appoint.Appointments(session)
    appointments_list = await appointment_data_access.get_many(patient_id, appointments_from, appointments_to)
    appointments_number = await appointment_data_access.count(patient_id, appointments_from, appointments_to)
    return appointments_list, appointments_number
