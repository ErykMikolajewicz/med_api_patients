from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.databases.relational import create_connection_pool
import src.routers.appointments
import src.routers.account

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_connection_pool()
    yield
    await pool.close()

app.include_router(src.routers.appointments.router)
app.include_router(src.routers.account.router)


def main():
    uvicorn.run(app, host='0.0.0.0', port=8009)


if __name__ == '__main__':
    main()
