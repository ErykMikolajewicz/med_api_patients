from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class Appointment(BaseModel):
    doctor_id: UUID
    start: datetime
    end: datetime


class AppointmentCreate(BaseModel):
    doctor_id: UUID
    start: datetime
    end: datetime
    patient_id: UUID
