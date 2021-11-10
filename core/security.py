from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
from jose import jwt
import datetime

from core.config import ACCESS_TOKEN_EXPIRE, SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    """ Хэширует пароль пользователя """
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    """ Проверяет пароль пользователя """
    return pwd_context.verify(password, hash)


def create_access_token(data: dict) -> str:
    """ Генерирует токен для пользователя """
    to_encode = data.copy()
    print(datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE))
    to_encode.update({'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE)})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def decode_access_token(token: str):
    """ Декодирует токен авторизованного пользователя """
    try:
        encode_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except jwt.JWSError:
        return None
    return encode_token


class JwtBearer(HTTPBearer):
    """ Класс для проверки авторизации пользователя """
    def __init__(self,auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, *args, **kwargs):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            token = decode_access_token(credentials.credentials)
            if not token:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Неправильный токен авторизации')
            return credentials.credentials
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Неправильный токен авторизации')
