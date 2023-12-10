from typing import Any

from asyncpg import pool


class Patients:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_patient: dict[str, Any]):
        pass

    # Probably unnecessary endpoint
    async def get_by_login(self, login: str):
        pass

    async def partial_update(self, id_: int, patient: dict[str, Any]):
        pass
    
    async def delete_account(self, id_: int) -> int:
        pass

    async def get_by_username(self, username):
        pass
