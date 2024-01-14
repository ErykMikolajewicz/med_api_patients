from datetime import date
from uuid import UUID

from asyncpg import pool


class Specialists:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def get_many(self, role_id: int | None):
        specialists_list = await self.connection_pool.fetchrow(
            "SELECT * FROM patients.get_specialist_list($1)", role_id)
        return specialists_list

    async def get_working_time(self, specialist_id: UUID, visit_date: date):
        specialist_working_time = await self.connection_pool.fetchrow(
            "SELECT * FROM patients.get_specialist_working_time($1, $2)", specialist_id, visit_date)
        return specialist_working_time
