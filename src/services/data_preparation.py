from typing import Any
from uuid import UUID

from src.services.security import hash_password


def prepare_new_user(user: dict[str, Any]) -> dict[str, Any]:
    hashed_password = hash_password(user['password'])
    user['hashed_password'] = hashed_password
    del user['password']
    del user['confirm_password']
    return user
