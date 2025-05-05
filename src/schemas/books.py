"""Модуль для определения схемы книги."""
from pydantic import BaseModel, Field



class BookSchema(BaseModel):
    """Схема для книги."""
    title: str = Field(description="Название")
    author: str = Field(description="Автор")
    year: int = Field(description="Год издания", ge=0, le=2025)
    pages: int = Field(description="Количество страниц", ge=0)
    class Config:
        """Пример заполнения."""
        json_schema_extra = {
            "example": {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "year": 1960,
                "pages": 12
            }
        }


class BookGetSchema(BookSchema):
    """Схема для получения информации о книге с идентификатором."""
    id: int = Field(description="Уникальный идентификатор")
