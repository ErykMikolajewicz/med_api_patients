from contextlib import asynccontextmanager
import ssl

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import src.routers.appointments
import src.routers.account
import src.routers.specialist
import src.routers.messages
from src.databases.relational import connect_to_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await connect_to_db()
    yield
    await connection.close()

app = FastAPI(lifespan=lifespan)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain('./certificate.pem', keyfile='./privatekey.pem')

app.include_router(src.routers.appointments.router)
app.include_router(src.routers.account.router)
app.include_router(src.routers.specialist.router)
app.include_router(src.routers.messages.router)


@app.get("/", response_class=RedirectResponse)  # to see docs after click startup link
async def redirect_fastapi():
    return "https://localhost:8008/docs"
