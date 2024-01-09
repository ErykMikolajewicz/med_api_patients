from typing import Optional, Any, Literal
from datetime import date, timedelta

from pydantic import BaseModel, Field, field_validator, model_validator


class AccountBase(BaseModel):
    telephone: Optional[str] = Field(None, min_length=9, max_length=13, pattern=r'^\d{9}$|^\+\d{10,12}$')
    email: Optional[str] = Field(None, min_length=5, max_length=255)
    address: Optional[str] = Field(None)


class AccountData(AccountBase):
    login: str = Field(min_length=2, max_length=155)
    name: str = Field(min_length=2, max_length=155)
    surname: str = Field(min_length=2, max_length=255)
    sex: Literal['male', 'female', 'intersex']
    pesel_or_identifier: str = Field(min_length=3, max_length=36)
    birth_date: date


class AccountCreate(AccountData):
    password: str = Field(min_length=8, max_length=36, pattern=r'\d.*[A-Z]|[A-Z].*\d')
    confirm_password: str = Field(min_length=8, max_length=36, pattern=r'\d.*[A-Z]|[A-Z].*\d')

    @field_validator('birth_date')  # PyCharm raise warning, but it's follow Pydantic documentation
    @classmethod
    def valid_birthdate(cls, birth_date: date) -> date:
        life_span = timedelta(days=125*365)
        current_date = date.today()
        if birth_date < current_date - life_span:
            raise ValueError('Birth date to low!')
        elif birth_date > current_date:
            raise ValueError('Birth date to big!')
        return birth_date

    @model_validator(mode='before')  # PyCharm raise warning, but it's follow Pydantic documentation
    @classmethod
    def confirm_password(cls, values: Any) -> Any:
        if values['password'] == values['confirm_password']:
            return values
        else:
            raise ValueError('Passwords don\'t match!')
