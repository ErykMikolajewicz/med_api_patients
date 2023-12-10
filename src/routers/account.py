from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status, Request

from src.services.authentication import authenticate, create_jwt_token, validate_token

router = APIRouter(tags=['accounts'])


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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")
Token = Annotated[str, Depends(oauth2_scheme)]


def token_authentication(token: Token, request: Request):
    validation_result = validate_token(token)
    if validation_result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    request.state.user_id = validation_result
