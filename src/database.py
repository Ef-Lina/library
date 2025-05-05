"""Модуль для работы с базой данных библиотеки."""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase



# Создаем асинхронный движок для работы с SQLite
engine = create_async_engine('sqlite+aiosqlite:///library.db')


# Создаем асинхронный сеанс для работы с базой данных
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Возвращает асинхронный сеанс для работы с базой данных."""
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    """Базовый класс для декларативного определения моделей базы данных."""
    pass


async def create_tables():
    """Создает таблицы в базе данных на основе определенных моделей."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async  def delete_tables():
    """Удаляет все таблицы из базы данных."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
