from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status

from core.security import verify_password, create_access_token
from endpoints.depends import get_user_repository
from models.token import Token, Login
from models.user import UserIn, User
from repositories.users import UserRepository

router = APIRouter()


@router.post('/register', response_model=User)
async def create(user: UserIn, users: UserRepository = Depends(get_user_repository)):
    """ Хендлер регистрации пользователя """
    try:
        return await users.create_user(u=user)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Пользователь с таким email уже зарегистрирован')


@router.post('/login', response_model=Token)
async def login(login: Login, users: UserRepository = Depends(get_user_repository)):
    """ Хендлер авторизации пользователя """
    user = await users.get_by_email(login.email)
    if not user or not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неправильный логин или пароль')
    return Token(
        access_token=create_access_token({'sub': user.email}),
        token_type='Bearer'
    )