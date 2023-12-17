from typing import Any, Annotated

from fastapi import APIRouter, Depends, Response, Request
from asyncpg import Pool

from src.routers.account import token_authentication
from src.domain.appointments import Appointment
from src.databases.relational import get_session
import src.repositories.appointments as repo_appoint

router = APIRouter(tags=['appointments'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]


@router.post("/appointments")
async def add_appointment(appointment: Appointment, session: AsyncPool, response: Response, request: Request):
    patient_id = request.state.patient_id
    appointment: dict[str, Any] = appointment.model_dump()
    appointment['patient_id'] = patient_id
    async with session.acquire():
        appointment_data_access = repo_appoint.Appointments(session)
        new_appointment = await appointment_data_access.add(appointment)
    appointment_id = new_appointment.id
    response.headers["Location"] = f"/appointments/{appointment_id}"
    return new_appointment
