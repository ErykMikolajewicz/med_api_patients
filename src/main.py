from contextlib import asynccontextmanager
import ssl

from fastapi import FastAPI
import uvicorn

from src.databases.relational import connect_to_db
import src.routers.appointments
import src.routers.account


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


def main():
    uvicorn.run(app, host='0.0.0.0', port=8009)


if __name__ == '__main__':
    main()
