from pydantic import BaseModel, Field, EmailStr
from typing import Union


class UserSchema(BaseModel):
    email: EmailStr = Field(description="Адрес электронной почты")
    password: Union[str , None] = Field(description="Пароль")
    name: str = Field(description="Имя")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Ванюша",
                "email": "van@exmpl.com",
                "password": "pass"
            }
        }