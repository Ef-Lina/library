from fastapi import APIRouter, status, HTTPException, Depends
from src.api.dependencies import SessionDep
from src.schemas.users import UserSchema
from src.schemas import users
    #, UserGetSchema
from src.models.users import UserModel
from sqlalchemy import select
from typing import List
from sqlalchemy.exc import IntegrityError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.auth import auth_handler

# from passlib.context import CryptContext
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


router = APIRouter(prefix="/auth",
    tags=["Безопасность 🗝️"],
                   )


@router.post("/signup", summary="Регистрация", status_code=status.HTTP_201_CREATED)
async def add_user(data:UserSchema, session: SessionDep):
    """
    Эндпоинт для добавления нового пользователя
    """

    new_user = UserModel(
        name = data.name,
        email = data.email,
        password = data.password
    )
    session.add(new_user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким email уже существует.")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return {"success": True, "message": "Регистрация прошла успешно"}


@router.post("/login", status_code=status.HTTP_200_OK,
             summary="Войти в систему")
async def user_login(session: SessionDep, login_attempt_data: OAuth2PasswordRequestForm = Depends()):
    statement = (select(UserModel)
                 .where(UserModel.email == login_attempt_data.username))
    result = await session.execute(statement)
    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"UserSchema {login_attempt_data.username} not found"
        )
    if existing_user.password == login_attempt_data.password:
        access_token = auth_handler.create_access_token(
            existing_user.user_id
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wrong password for user {login_attempt_data.username}"
        )




        # async def user_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(), session: SessionDep):
        #     statement = (select(users.UserSchema)
        #                  .where(users.UserSchema.email == login_attempt_data.username))
        #     existing_user = session.exec(statement).first()
        #
        #     if not existing_user:
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail=f"UserSchema {login_attempt_data.username} not found"
        #         )
        #     if verify_password(login_attempt_data.password, existing_user.password):

