"""Модуль для определения конфигурации приложения."""
from pydantic_settings import BaseSettings


class SettingsSchema(BaseSettings):
    """Схема для конфигурации приложения."""
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        """Заполнение из файла"""
        env_file = ".env"

settings = SettingsSchema()
