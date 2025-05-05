from pydantic_settings import BaseSettings


class SettingsSchema(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = SettingsSchema()