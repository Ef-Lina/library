"""Модуль для работы с репозиторием книг и аннотаций."""
from typing import List, Dict, Any
from sqlalchemy import select, join
from src.database import new_session
from src.models.books import BookModel
from src.schemas.annotation import AnnotateSchema
from src.models.annotation import AnnotateModel



class BookRepository:
    """Репозиторий для управления книгами и аннотациями."""
    @classmethod
    async def add_one(cls, data: AnnotateSchema)-> int:
        """Добавляет одну аннотацию книги и возвращает ее ID."""
        async with new_session() as session:
            book_dict = data.model_dump()

            book = AnnotateModel(**book_dict)
            session.add(book)
            await session.flush()
            await session.commit()

            return book.annotation_id


    @classmethod
    async def find_all(cls) -> List[Dict[str, Any]]:
        """Находит все книги с их аннотациями."""
        async with new_session() as session:
            query = (
                select(BookModel, AnnotateModel)
                .select_from(join(BookModel, AnnotateModel,
                                  BookModel.title == AnnotateModel.title))
            )
            result = await session.execute(query)
            rows = result.fetchall()
            book_with_annotations = []
            for book, annotation in rows:
                book_dict = {
                    "author": book.author,
                    "title": book.title,
                    "year": book.year,
                    "annotation": None
                }
                if annotation:
                    book_dict["annotation"] = annotation.annotation
                book_with_annotations.append(book_dict)

            return book_with_annotations
