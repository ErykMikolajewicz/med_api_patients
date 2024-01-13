from typing import Any
from uuid import UUID

from asyncpg import pool


class Appointments:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_appointment: dict[str, Any]):
        new_appointment = await self.connection_pool.fetchrow(
            "SELECT * FROM patients.add_appointment($1, $2, $3, $4)", *new_appointment.values()
        )
        return new_appointment

    async def get_many(self, patient_id, appointments_from, appointments_to):
        appointments_list = await self.connection_pool.fetch(
            "SELECT * FROM patients.get_appointments_list($1, $2, $3)", patient_id, appointments_from,
            appointments_to)
        return appointments_list

    async def count(self, patient_id, appointment_from, appointment_to):
        appointments_number = await self.connection_pool.fetchval(
            "SELECT * FROM patients.count_appointments($1, $2, $3)", patient_id, appointment_from,
            appointment_to)
        return appointments_number

    async def delete(self, appointment_id: UUID):
        pass
