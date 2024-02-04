from typing import Any, Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Query
from asyncpg import Pool
import asyncpg.exceptions

from src.routers.account import token_authentication
from src.domain.models.appointments import Appointment
from src.databases.relational import get_session
import src.services.appointment as srv_appointment
from src.services.general import prepare_pagination_link
from src.domain.models.general import pagination_dependency
import src.exceptions.appointments as appointment_exc

router = APIRouter(tags=['appointments'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]
DatetimeQuery = Annotated[datetime | None, Query()]


@router.get("/appointments")
async def get_appointments(session: AsyncPool, pagination: pagination_dependency, response: Response, request: Request,
                           appointments_from: DatetimeQuery = None, appointments_to: DatetimeQuery = None):
    patient_id = request.state.patient_id
    async with session.acquire() as session:
        appointments, appointments_number = await srv_appointment.get_list(session, patient_id, appointments_from,
                                                                           appointments_to)
    if not appointments:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    for appointment in appointments:
        appointment = dict(appointment)
        appointment['location'] = f"/appointments/{appointment['id']}"
    link_base = '<appointments?page-number={0}&page-size={1}>; {2}'
    links = prepare_pagination_link(link_base, pagination, appointments_number)
    response.headers["Link"] = links
    return appointments


@router.post("/appointments", status_code=status.HTTP_201_CREATED)
async def schedule_appointment(appointment: Appointment, session: AsyncPool, response: Response, request: Request):
    patient_id = request.state.patient_id
    appointment: dict[str, Any] = appointment.model_dump()
    appointment['patient_id'] = patient_id
    async with session.acquire() as session:
        try:
            new_appointment = await srv_appointment.add(session, appointment)
        except asyncpg.exceptions.RaiseError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Chosen visit date is engaged.')
        except appointment_exc.InvalidVisitDate:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Chosen visit date is not available')
    appointment_id = new_appointment['id']
    response.headers["Location"] = f"/appointments/{appointment_id}"
    return new_appointment


@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_appointment(appointment_id: str, session: AsyncPool, request: Request):
    patient_id = request.state.patient_id
    async with session.acquire() as session:
        try:
            await srv_appointment.delete(session, appointment_id, patient_id)
        except appointment_exc.NotFound:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except appointment_exc.InsufficientPrivileges:
            # Different business logic from appointment_exc.NotFound,
            # to consider logging this as security violation try
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        except appointment_exc.TooShortTimeToCancel:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Too late to cancel appointment')



