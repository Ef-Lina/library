from pydantic import BaseModel, Field



class BookSchema(BaseModel):
    title: str = Field(description="Название")
    author: str = Field(description="Автор")
    year: int = Field(description="Год издания")
    class Config:
        json_schema_extra = {
            "example": {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "year": 1960
            }
        }


class BookGetSchema(BookSchema):
    id: int = Field(description="Уникальный идентификатор")