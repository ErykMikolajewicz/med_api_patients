from datetime import datetime, date

from fastapi import HTTPException, status

import src.repositories.appointments as repo_appoint
import src.repositories.doctors_working_time as repo_working_time
from src.domain.services.appointment_scheduling import validate_doctors_working_hour


async def add_appointment(session, appointment):
    doctor_id = appointment['doctor_id']
    visit_date: datetime = appointment['start']
    visit_date: date = visit_date.date()

    working_time_data_access = repo_working_time.DoctorsWorkingTime(session)
    doctor_working_time = await working_time_data_access.get_working_time(doctor_id, visit_date)

    is_valid_visit_time = await validate_doctors_working_hour(appointment, doctor_working_time)
    if not is_valid_visit_time:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Chosen visit date is not available')

    appointment_data_access = repo_appoint.Appointments(session)
    new_appointment = await appointment_data_access.add(appointment)
    return new_appointment
