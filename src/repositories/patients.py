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
    async def get_by_login(self, login: str):
        pass

    async def partial_update(self, id_: int, patient: dict[str, Any]):
        pass
    
    async def delete_account(self, id_: int) -> int:
        pass

    async def get_by_username(self, username):
        pass
