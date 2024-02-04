from datetime import datetime, date

import src.repositories.appointments as repo_appoint
import src.repositories.specialists as repo_working_time
from src.domain.services.appointment_scheduling import validate_specialist_working_time, check_can_be_canceled
import src.exceptions.appointments as appointment_exc


async def add(session, appointment):
    specialist_id = appointment['specialist_id']
    visit_date: datetime = appointment['start']
    visit_date: date = visit_date.date()

    working_time_data_access = repo_working_time.Specialists(session)
    doctor_working_time = await working_time_data_access.get_working_time(specialist_id, visit_date)

    is_valid_visit_time = validate_specialist_working_time(appointment, doctor_working_time)
    if not is_valid_visit_time:
        raise appointment_exc.InvalidVisitDate

    appointment_data_access = repo_appoint.Appointments(session)
    new_appointment = await appointment_data_access.add(appointment)
    return new_appointment


async def get_list(session, patient_id, appointments_from, appointments_to):
    appointment_data_access = repo_appoint.Appointments(session)
    appointments_list = await appointment_data_access.get_many(patient_id, appointments_from, appointments_to)
    appointments_number = await appointment_data_access.count(patient_id, appointments_from, appointments_to)
    return appointments_list, appointments_number


async def delete(session, appointment_id, patient_id):
    appointment_data_access = repo_appoint.Appointments(session)
    appointment = await appointment_data_access.get(appointment_id)
    if appointment is None:
        raise appointment_exc.NotFound
    if appointment['id'] != patient_id:
        raise appointment_exc.InsufficientPrivileges
    if check_can_be_canceled(appointment):
        await appointment_data_access.delete(appointment_id)
    else:
        raise appointment_exc.TooShortTimeToCancel


