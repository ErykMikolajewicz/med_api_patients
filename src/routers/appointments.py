from typing import Any, Annotated

from fastapi import APIRouter, Depends, Response, Request
from asyncpg import Pool

from src.routers.account import token_authentication
from src.domain.models.appointments import Appointment
from src.databases.relational import get_session
from src.services.appointment import add_appointment

router = APIRouter(tags=['appointments'], dependencies=[Depends(token_authentication)])

AsyncPool = Annotated[Pool, Depends(get_session)]


@router.post("/appointments")
async def schedule_appointment(appointment: Appointment, session: AsyncPool, response: Response, request: Request):
    patient_id = request.state.patient_id
    appointment: dict[str, Any] = appointment.model_dump()
    appointment['patient_id'] = patient_id
    async with session.acquire() as session:
        new_appointment = await add_appointment(session, appointment)
    appointment_id = new_appointment['id']
    response.headers["Location"] = f"/appointments/{appointment_id}"
    return new_appointment
