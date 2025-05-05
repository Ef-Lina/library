from fastapi import APIRouter, status, Form, Depends
from src.api.dependencies import SessionDep
from src.schemas.books import BookSchema, BookGetSchema
from src.models.books import BookModel
from sqlalchemy import select
from typing import List
from typing_extensions import Annotated
from src.repository import BookRepository

router = APIRouter(prefix="/books_2",
    tags=["Книги 📚"],
                   )




@router.post("/", summary="Добавить новую книгу", status_code=status.HTTP_201_CREATED)
async def add_book(book: Annotated[BookSchema, Depends()],session: SessionDep):
    """
    Эндпоинт для боьавления новой книги в базу данных
    """
    book_id = await BookRepository.add_one(book)
    return {"ok": True, "book_id": book_id}


@router.get("/", summary="Получить все книги", status_code=status.HTTP_200_OK)
async def get_books():
    """
    Эндпоинт для получения всех книг из базы данных
    """
    books = await BookRepository.find_all()
    return {"books":books}
