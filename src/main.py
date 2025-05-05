from fastapi import FastAPI
from src.api import main_router
from contextlib import asynccontextmanager
from src.database import delete_tables, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")

app = FastAPI(
    lifespan=lifespan,
    title="Библиотека",
    description="Система управления книгами"
)
app.include_router(main_router)
