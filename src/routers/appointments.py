from typing import Any, Annotated
from datetime import datetime

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Query
from asyncpg import Pool
from asyncpg.exceptions import RaiseError

from src.routers.account import token_authentication
from src.domain.models.appointments import Appointment
from src.databases.relational import get_session
from src.services.appointment import add_appointment, get_appointments_list
from src.services.general import prepare_pagination_link
from src.domain.models.general import pagination_dependency

router = APIRouter(tags=['appointments'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]
DatetimeQuery = Annotated[datetime | None, Query()]


@router.get("/appointments")
async def get_appointments(session: AsyncPool, pagination: pagination_dependency, response: Response, request: Request,
                           appointments_from: DatetimeQuery = None, appointments_to: DatetimeQuery = None):
    patient_id = request.state.patient_id
    async with session.acquire() as session:
        appointments, appointments_number = await get_appointments_list(session, patient_id, appointments_from,
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
            new_appointment = await add_appointment(session, appointment)
        except RaiseError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Chosen visit date is engaged.')
    appointment_id = new_appointment['id']
    response.headers["Location"] = f"/appointments/{appointment_id}"
    return new_appointment



