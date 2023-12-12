from typing import Any

from asyncpg import pool


class Patients:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_patient: dict[str, Any]):
        new_patient = await self.connection_pool.fetchval(
            "SELECT patients.add_patient($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", *new_patient.values()
        )
        return new_patient

    # Probably unnecessary endpoint
    async def get_authentication_data(self, login: str) -> dict[str, Any]:
        authentication_data = await self.connection_pool.fetchval(
            "SELECT patients.get_authentication_data($1)", login
        )
        return authentication_data
