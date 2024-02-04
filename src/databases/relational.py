import os
import asyncpg


POSTGRES_PASSWORD_FILE = os.environ['POSTGRES_PASSWORD_FILE']
with open(POSTGRES_PASSWORD_FILE, 'r') as file:
    postgres_password = file.read()

ENV = os.environ['ENV']
if ENV == 'LOCAL':
    host = 'localhost'
elif ENV == 'DOCKER':
    host = 'postgres_database'
else:
    raise Exception('Invalid environment config!')

pool: asyncpg.Pool | None = None


async def connect_to_db():
    global pool
    pool = await asyncpg.pool.create_pool(host=host,
                                          port=5432,
                                          user='patient_user',
                                          database='postgres',
                                          password=postgres_password)
    return pool


async def get_session() -> asyncpg.pool.Pool:
    return pool
