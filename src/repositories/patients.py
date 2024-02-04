from typing import Any
from uuid import UUID

from asyncpg import pool


class Patients:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def add(self, new_patient: dict[str, Any]):
        new_patient = await self.connection_pool.fetchrow(
            'SELECT * FROM patients.add_patient($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
            *new_patient.values()
        )
        return new_patient

    # Probably unnecessary endpoint
    async def get_authentication_data(self, login: str) -> dict[str, Any]:
        authentication_data = await self.connection_pool.fetchrow(
            'SELECT * FROM patients.get_authentication_data($1)', login
        )
        return authentication_data

    async def verify_email(self, patient_id: UUID) -> str:
        email = await self.connection_pool.fetchval('SELECT * FROM patients.verify_email($1)', patient_id)
        return email


class EmailVerification:
    def __init__(self, connection_pool: pool.Pool):
        self.connection_pool = connection_pool

    async def get(self, verification_parameter: str):
        email_verification_data = await self.connection_pool.fetchrow(
            'SELECT * FROM patients.check_email_verification($1)', verification_parameter)
        return email_verification_data

    # Probably unnecessary endpoint
    async def add(self, verification_parameter: str, patient_id: UUID):
        verification_parameter = await self.connection_pool.fetchrow(
            'SELECT * FROM patients.add_email_verification($1, $2)', verification_parameter, patient_id)
        return verification_parameter
