from typing import Any
from uuid import UUID
from datetime import date

from asyncpg import pool


class Messages:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_message: dict[str, Any]):
        new_message = await self.connection_pool.fetchrow(
            'SELECT * FROM patients.add_message($1, $2, $3, $4)', *new_message.values()
        )
        return new_message

    async def get(self, message_id: UUID):
        message = await self.connection_pool.fetch(
            'SELECT * FROM patients.get_message($1)', message_id)
        return message

    async def get_list(self, patient_id: UUID, specialist_id: UUID | None, messages_from: date | None,
                       messages_to: date | None):
        messages_list = await self.connection_pool.fetch(
            'SELECT * FROM patients.get_messages_list($1, $2, $3, $4)', patient_id, messages_from,
            specialist_id, messages_to)
        return messages_list

    async def count(self, patient_id: UUID, specialist_id: UUID | None, messages_from: date | None,
                    messages_to: date | None):
        messages_number = await self.connection_pool.fetchval(
            'SELECT * FROM patients.count_messages($1, $2, $3, $4)', patient_id, specialist_id, messages_from,
            messages_to)
        return messages_number
