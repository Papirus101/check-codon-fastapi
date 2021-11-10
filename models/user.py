from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr
import datetime


class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    hashed_password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    password2: constr(min_length=8)

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
