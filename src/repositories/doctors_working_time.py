from datetime import date
from uuid import UUID

from asyncpg import pool


class DoctorsWorkingTime:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def get_working_time(self, doctor_id: UUID, visit_date: date):
        doctor_working_time = await self.connection_pool.fetchrow(
            "SELECT * FROM patients.get_doctor_working_time($1, $2)", doctor_id, visit_date)
        return doctor_working_time
