from uuid import UUID
from datetime import datetime, timedelta

from jose import jwt, JWTError

from src.services.security import verify_password, TOKEN_EXPIRE_MINUTES, JWT_KEY, JWT_ALGORITHM
from src.repositories.patients import Patients


async def authenticate(login, password, session) -> tuple[bool | None, UUID | None]:
    patients_repo = Patients(session)
    authentication_data = await patients_repo.get_authentication_data(login)
    patient_id = authentication_data['id']
    if patient_id:
        return verify_password(password, authentication_data['hashed_password']), patient_id
    return None, None


def create_jwt_token(token_data: dict) -> str:
    expires_after = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    expire_datetime = datetime.now() + expires_after
    token_data['expire'] = expire_datetime
    jwt_token = jwt.encode(token_data, JWT_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


def validate_token(token) -> UUID | None:
    try:
        decoded_token = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        return None
    token_expire: datetime = decoded_token.get("expire")
    if token_expire < datetime.now():
        raise Exception('TOKEN EXPIRED!!!')
    user_id: UUID = decoded_token.get("subject")
    return user_id
