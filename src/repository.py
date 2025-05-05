from src.database import new_session
from src.models.books import BookModel
from src.schemas.books import BookSchema
from sqlalchemy import select



class BookRepository:
    @classmethod
    async def add_one(cls, data: BookSchema)-> int:
        async with new_session() as session:
            book_dict = data.model_dump()

            book = BookModel(**book_dict)
            session.add(book)
            await session.flush()
            await session.commit()
            return book.id


    @classmethod
    async def find_all(cls):
        async with new_session() as session:
            query = select(BookModel)
            result = await session.execute(query)
            book_models = result.scalars().all()
            return book_models
