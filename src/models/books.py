"""Модуль для определения модели книги в базе данных."""
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base




class BookModel(Base):
    """Модель книги для хранения информации
    о книгах в базе данных."""
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    year: Mapped[int]
    pages: Mapped[int]
