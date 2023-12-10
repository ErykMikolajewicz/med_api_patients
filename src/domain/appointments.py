import uuid
import datetime

from pydantic import BaseModel, Field


class AppointmentBase(BaseModel):
    doctor_id: int = Field(gt=0)
    start: datetime.datetime
    end: datetime.datetime


class Appointment(AppointmentBase):
    id: uuid.uuid4
