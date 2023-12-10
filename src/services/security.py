import hashlib
import json
import os
import random
import string
import secrets


JWT_SECRETS_FILE = os.environ["JWT_SECRETS_FILE"]
with open(JWT_SECRETS_FILE, 'r') as jwt_secrets:
    jwt_secrets = json.load(jwt_secrets)


JWT_KEY = jwt_secrets['jwt_key']
JWT_ALGORITHM = jwt_secrets['algorithm']
TOKEN_EXPIRE_MINUTES = jwt_secrets['expire_time_minutes']


salt_file = os.environ["SALT_FILE"]
with open(salt_file, 'r') as file:
    SALT = file.read()


def hash_password(password: str) -> bytes:
    password_with_salt = SALT + password
    hash_ = hashlib.sha256(password_with_salt.encode("utf-8"), usedforsecurity=True)
    hashed_password = hash_.digest()
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    to_check = hash_password(password)
    return secrets.compare_digest(hashed_password, to_check)


def create_and_hash_random_password() -> (str, bytes):
    characters = string.printable
    password = ''.join(secrets.choice(characters) for _ in range(34))

    big_letters = string.ascii_uppercase
    random_value = random.randint(0, 25)
    password += big_letters[random_value]

    digits = string.digits
    random_value = random.randint(0, 9)
    password += digits[random_value]

    password_hash = hash_password(password)
    return password, password_hash
