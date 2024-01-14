from typing import Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, model_validator


class Appointment(BaseModel):
    specialist_id: UUID
    start: datetime
    end: datetime

    @model_validator(mode='after')  # PyCharm raise warning, but it's follow Pydantic documentation
    @classmethod
    def check_date_validation(cls, values: Any) -> Any:
        start = values.start
        end = values.end
        if start <= datetime.now():
            raise ValueError('Invalid start date.')
        if end <= start:
            raise ValueError('Invalid end date.')
        return values


class AppointmentCreate(Appointment):
    patient_id: UUID
