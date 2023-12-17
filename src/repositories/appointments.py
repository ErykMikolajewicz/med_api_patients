from typing import Any
from uuid import UUID

from asyncpg import pool


class Appointments:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_appointment: dict[str, Any]):
        print(new_appointment)
        new_appointment = await self.connection_pool.fetchrow(
            "SELECT * FROM patients.add_appointment($1, $2, $3, $4)", *new_appointment.values()
        )
        return new_appointment

    async def delete(self, appointment_id: UUID):
        pass
