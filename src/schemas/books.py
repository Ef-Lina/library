from pydantic import BaseModel, Field



class BookSchema(BaseModel):
    title: str = Field(description="Название")
    author: str = Field(description="Автор")
    year: int = Field(description="Год издания", ge=0, le=2025)
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