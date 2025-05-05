"""Модуль для определения схемы пользователя."""
from typing import Union
from pydantic import BaseModel, Field, EmailStr



class UserSchema(BaseModel):
    """Схема для пользователя."""
    email: EmailStr = Field(description="Адрес электронной почты")
    password: Union[str , None] = Field(description="Пароль")
    name: str = Field(description="Имя")

    class Config:
        """Пример заполнения"""
        json_schema_extra = {
            "example": {
                "name": "Ванюша",
                "email": "van@exmpl.com",
                "password": "pass"
            }
        }
