from fastapi import APIRouter
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.schemas.books import BookSchema, BookGetSchema
from src.models.books import BookModel
from sqlalchemy import select
from typing import List


router = APIRouter()

@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@router.post("/books")
async def add_book(data: BookSchema, session: SessionDep):
    new_book = BookModel(
        title = data.title,
        author = data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@router.get("/books")
async def get_books(session: SessionDep) -> List[BookGetSchema]:
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()
    print(f"{books}")
    return books
