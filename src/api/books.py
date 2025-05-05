from fastapi import APIRouter, status, HTTPException
from src.api.dependencies import SessionDep
from src.schemas.books import BookSchema, BookGetSchema
from src.models.books import BookModel
from sqlalchemy import select
from typing import List
from sqlalchemy.exc import IntegrityError



router = APIRouter(prefix="/books_1",
    tags=["Книги 📚"],
                   )




@router.post("/", summary="Добавить новую книгу", status_code=status.HTTP_201_CREATED)
async def add_book(data:BookSchema, session: SessionDep):
    """
    Эндпоинт для боьавления новой книги в базу данных
    """
    new_book = BookModel(
        title = data.title,
        author = data.author,
        year = data.year
    )

    session.add(new_book)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Книга с таким названием уже существует.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return {"success": True, "message": "Книга успешно добавлена"}


@router.get("/", summary="Получить все книги", status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep) -> List[BookGetSchema]:
    """
    Эндпоинт для получения всех книг из базы данных
    """
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()
    if books is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Библиотека пуста")
    return books


@router.get("/{book_id}", summary="Получить конкретную книгу", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int, session: SessionDep) -> BookGetSchema:
    """
    Эндпоинт для получения конкретной книги из базы данных
    """
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    book = result.scalars().first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book


@router.patch("/{book_id}", summary="Изменить данные о книге", status_code=status.HTTP_200_OK)
async def update_book_by_id(book_id: int, data:BookSchema, session: SessionDep):
    """
    Эндпоинт для изменения данных о книге в базе данных
    """
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    # Обновляем поля книги
    book.title = data.title
    book.author = data.author
    book.year = data.year
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return {"success": True, "message": "Данные книги успешно обновлены"}


@router.delete("/{book_id}", summary="Удалить книгу", status_code=status.HTTP_200_OK)
async def delete_book_by_id(book_id: int, session: SessionDep):
    """
    Эндпоинт для удаления книги из базы данных
    """
    query = select(BookModel).where(BookModel.id == book_id)
    result = await session.execute(query)
    book = result.scalars().first()

    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    await session.delete(book)  # Удаляем книгу
    await session.commit()

    return {"success": True, "message": "Книга успешно удалена"}