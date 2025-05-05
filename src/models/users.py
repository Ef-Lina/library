from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from typing import Union



class UserModel(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Union[str, None]]
    name: Mapped[str]