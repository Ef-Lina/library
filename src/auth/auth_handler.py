"""Модуль для аутентификации и управления токенами."""
from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated
from sqlmodel import select  # Уберите неиспользуемый импорт Session
from src.schemas.config import settings
from src.api.dependencies import SessionDep
from src.models import users as schema_users



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password):
    """Хеширует пароль с использованием bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Проверяет соответствие введённого пароля и хешированного пароля."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict,
                        expires_delta: Union[timedelta, None] = None):
    """Создает JWT токен с заданными данными и временем истечения."""
    to_encode = data.copy()
    if expires_delta:
        expire = (datetime.now(timezone.utc) +
                  expires_delta)
    else:
        expire = (datetime.now(timezone.utc) +
                  timedelta(minutes=15))

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,
                             settings.secret_key,
                             algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db_session: SessionDep):
    """Получает текущего пользователя на основе предоставленного токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception from e

    statement = (select(schema_users.UserModel)
                 .where(schema_users.UserModel.email == username))
    user = await db_session.execute(statement)
    user = user.scalars().first()

    if user is None:
        raise credentials_exception
    return user
