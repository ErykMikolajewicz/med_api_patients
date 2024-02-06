from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    specialist_id: UUID
    title: str
    message: str
