from datetime import date
from uuid import UUID

from src.repositories.messages import Messages


async def add(session, message):
    messages_repo = Messages(session)
    new_message = await messages_repo.add(message)
    return new_message


async def get_list(session, patient_id: UUID, specialist_id: UUID | None, messages_from: date | None,
                   messages_to: date | None):
    messages_repo = Messages(session)
    messages_list = await messages_repo.get_list(patient_id, specialist_id, messages_from, messages_to)
    messages_number = await messages_repo.count(patient_id, specialist_id, messages_from, messages_to)
    return messages_list, messages_number


async def get(session, patient_id, message_id):
    messages_repo = Messages(session)
    message = await messages_repo.get(message_id)
    return message
