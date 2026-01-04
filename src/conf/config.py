from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:098765@localhost:5432/abcdef"
    SECRET_KEY_JWT: str = "1234567890"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME: EmailStr = "postgres@mail.com"
    MAIL_PASSWORD: str = "postgresmail"
    MAIL_FROM: str = "your_email@example.com"
    MAIL_PORT: int = 567234
    MAIL_SERVER: str = "postgresserver"
    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )


config = Settings()
