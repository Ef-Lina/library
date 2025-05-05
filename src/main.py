"""Модуль для настройки приложения FastAPI и управления жизненным циклом базы данных."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api import main_router
from src.database import delete_tables, create_tables



@asynccontextmanager
async def lifespan(application: FastAPI):
    """Управляет жизненным циклом приложения, очищая и создавая базу данных."""
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(
    lifespan=lifespan,
    title="🏛️ Библиотека",
    description="Система управления книгами"
)


app.include_router(main_router)
