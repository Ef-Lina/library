"""Модуль для определения зависимостей FastAPI."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated
from src.database import get_session



SessionDep = Annotated[AsyncSession, Depends(get_session)]
