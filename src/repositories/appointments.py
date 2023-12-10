from typing import Any

from asyncpg import pool


class Appointments:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add_appointment(self, new_appointment: dict[str, Any]):
        pass
