from pydantic import BaseModel



class BookSchema(BaseModel):
    title: str
    author: str
    year: int


class BookGetSchema(BookSchema):
    id: int