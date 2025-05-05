"""Модуль для работы с аннотациями книг."""
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from typing_extensions import Annotated
from src.schemas.annotation import AnnotateSchema
from src.models.users import UserModel
from src.repository import BookRepository
from src.auth.auth_handler import get_current_user



router = APIRouter(prefix="/books_2",
    tags=["Книги 📚"],
                   )

oauth2_scheme_1 = OAuth2PasswordBearer(tokenUrl="books_2/")


async def get_current_username(current_user: Annotated[UserModel,
                                Depends(get_current_user)]):
    """Проверка текущего пользователя по email."""
    username = current_user.email
    if username != "vanyusha@head.com":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


@router.post("/", summary="Добавить аннотацию книги",
             status_code=status.HTTP_201_CREATED)
async def add_annotation(book: Annotated[AnnotateSchema, Depends()],
                   current_user: str = Depends(get_current_username)):
    """
    Эндпоинт для добавления новой аннотации книги в базу данных.
    """
    try:
        annotation_id = await BookRepository.add_one(book)
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="У книги с таким названием "
                                   "уже есть аннотация.") from exc
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=str(e)) from e
    return {"ok": True, "message": "Аннотация книги успешно добавлена",
            "annotation_id": annotation_id}


@router.get("/", summary="Получить все книги с аннотациями",
            status_code=status.HTTP_200_OK)
async def get_books(current_user: str = Depends(get_current_username)):
    """
    Эндпоинт для получения всех книг из базы данных.
    """
    books = await BookRepository.find_all()
    return {"books":books}
