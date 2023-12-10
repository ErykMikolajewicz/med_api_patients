import os
import asyncpg


POSTGRES_PASSWORD_FILE = os.environ["POSTGRES_PASSWORD_FILE"]
with open(POSTGRES_PASSWORD_FILE, 'r') as file:
    postgres_password = file.read()

ENV = os.environ["ENV"]
if ENV == 'LOCAL':
    host = 'localhost/postgres'
elif ENV == 'DOCKER':
    host = 'postgres_database/postgres'
else:
    raise Exception('Invalid environment config!')

user = 'patient_user'

DATABASE_URL = f"postgresql://{user}:{postgres_password}@{host}"

pool: asyncpg.pool.Pool | None = None


async def create_connection_pool():
    global pool
    pool = await asyncpg.pool.create_pool(DATABASE_URL)
    return pool


def get_session() -> asyncpg.pool.Pool:
    return pool


session: asyncpg.pool.Pool = get_session()
