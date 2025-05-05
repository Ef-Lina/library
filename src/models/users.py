"""Модуль для определения модели пользователя в базе данных."""
from typing import Union
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class UserModel(Base):
    """Модель пользователя для хранения информации
    о пользователях в базе данных."""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Union[str, None]]
    name: Mapped[str]
