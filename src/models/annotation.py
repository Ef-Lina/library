"""Модуль для определения модели аннотаций в базе данных."""
from typing import Union
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base



class AnnotateModel(Base):
    """Модель аннотации для хранения аннотаций в базе данных."""
    __tablename__ = "annotations"

    annotation_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    annotation: Mapped[Union[str, None]]
