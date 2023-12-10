from typing import Annotated, Any

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from asyncpg import Pool

from src.services.authentication import authenticate, create_jwt_token, validate_token
from src.services.data_preparation import prepare_new_user
import src.repositories.patients as repo_pat
from src.domain.account import AccountCreate
from src.databases.relational import get_session

router = APIRouter(tags=['accounts'])
AsyncSessionDep = Annotated[Pool, Depends(get_session)]


@router.post("/login/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session):
    username = form_data.username
    password = form_data.password
    async with session.begin():
        user_id = await authenticate(username, password, session)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        access_token = create_jwt_token({"subject": user_id})
        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create/account")
async def create_account(patient: AccountCreate, session: AsyncSessionDep, response: Response):
    patient: dict[str, Any] = patient.model_dump()
    patient = prepare_new_user(patient)
    async with session.acquire():
        data_access = repo_pat.Patients(session)
        new_patient = await data_access.add(patient)
    print(new_patient)
    patient_id = new_patient['id']
    response.headers["Location"] = f"/patients/{patient_id}"
    return new_patient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")
Token = Annotated[str, Depends(oauth2_scheme)]


def token_authentication(token: Token, request: Request):
    validation_result = validate_token(token)
    if validation_result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    request.state.user_id = validation_result
