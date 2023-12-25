from typing import Any

import pytest
from pydantic import ValidationError

from src.domain.account import AccountCreate
from tests.helpers import RandomStringCreator


@pytest.fixture(scope="function")
def account_data(request):
    correct_data = {
        'login': 'login',
        'name': 'Marvin',
        'surname': 'Gothic',
        'sex': 'male',
        'pesel_or_identifier': 'MARVIN',
        'birth_date': '2021-12-10',
        'password': 'Password123',
        'confirm_password': 'Password123'
    }
    return correct_data


@pytest.mark.parametrize('invalid_date', ['2025-12-12', '1888-10-13', '1999-13-25', None])
def test_invalid_date(invalid_date, account_data: dict[str, Any]):
    account_data['birth_date'] = invalid_date
    with pytest.raises(ValidationError):
        AccountCreate.model_validate(account_data)


@pytest.mark.parametrize('invalid_sex', ['Male', 'other', None])
def test_invalid_sex(invalid_sex, account_data: dict[str, Any]):
    account_data['sex'] = invalid_sex
    with pytest.raises(ValidationError):
        AccountCreate.model_validate(account_data)


@pytest.mark.parametrize('not_matching_password', ['password123', 'Password 123', None])
def test_not_matching_password(not_matching_password, account_data: dict[str, Any]):
    account_data['confirm_password'] = not_matching_password
    with pytest.raises(ValidationError):
        AccountCreate.model_validate(account_data)


@pytest.mark.parametrize("field, invalid_length", [("login", 156), ('name', 156), ("surname", 256), ('sex', 11),
                                                   ('pesel_or_identifier', 37), ('email', 256)])
def test_add_too_length_field(field, invalid_length, account_data: dict[str, Any]):
    string_creator = RandomStringCreator(length=invalid_length)
    to_length_field = string_creator.create_string()
    account_data[field] = to_length_field
    with pytest.raises(ValidationError):
        AccountCreate.model_validate(account_data)
