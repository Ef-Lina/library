"""Модуль для вспомогательных инструментов API."""
from fastapi import Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer
from typing_extensions import Annotated
from src.auth.auth_handler import get_current_user
from src.models.users import UserModel

router = APIRouter(tags=["Вспомогательные инструменты 🔨️"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/test-auth")
def show_access_token(token: str = Depends(oauth2_scheme)):
    """Показать токен доступа."""
    return {"token": token}

@router.get("/me", response_model=int,
            summary="Получить ID вошедшего пользователя")
def read_users_me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    """Получить ID текущего пользователя."""
    return current_user.user_id
