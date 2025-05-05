"""Модуль для определения схемы аннотации книги."""
from pydantic import BaseModel, Field



class AnnotateSchema(BaseModel):
    """Схема для аннотации книги."""
    title: str = Field(description="Название")
    annotation: str = Field(description="Аннотация",
                            max_length=200)
