"""
Модуль тестирования функций аутентификации пользователя.

Этот модуль содержит тесты для проверки функциональности аутентификации пользователей,
включая регистрацию и получение текущего имени пользователя. Используется библиотека pytest
и асинхронные тесты с помощью pytest-asyncio.

Тесты:
-------
- test_get_current_username_valid_user: Проверяет, что функция возвращает имя пользователя,
  когда электронная почта совпадает.
- test_get_current_username_unauthorized_email: Проверяет, что функция вызывает HTTPException
  для неавторизованной электронной почты.
- test_get_current_username_empty_email: Проверяет обработку случая, когда у пользователя
  пустая электронная почта.
- test_add_user: Проверяет успешную регистрацию нового пользователя через API.
- test_signup: Проверяет процесс регистрации нового
    пользователя с использованием фейковых данных.
- test_login: Проверяет процесс входа пользователя с использованием фейковых данных.
"""

from fastapi import HTTPException, status
from fastapi.testclient import TestClient
import pytest
import faker
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.models.users import UserModel
from src.api.books_v2 import get_current_username
from src.database import create_tables



@pytest.mark.asyncio
async def test_get_current_username_valid_user():
    """
    Тестирует, что функция возвращает имя пользователя,
    когда электронная почта совпадает.
    """
    # Создание поддельного пользователя с определенной электронной почтой
    mock_user = UserModel(email="vanyusha@head.com")
    result = await get_current_username(mock_user)
    assert result == "vanyusha@head.com"


@pytest.mark.asyncio
async def test_get_current_username_unauthorized_email():
    """
    Тестирует, что функция вызывает HTTPException для
    неавторизованной электронной почты.
    """
    # Создание поддельного пользователя с другой электронной почтой
    mock_user = UserModel(email="different@email.com")

    # Expect an HTTPException to be raised
    with pytest.raises(HTTPException) as exc_info:
        await get_current_username(mock_user)

    # Additional assertions about the exception
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid authentication credentials"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}




@pytest.mark.asyncio
async def test_get_current_username_empty_email():
    """
    Тестирует обработку случая, когда у пользователя
    пустая электронная почта.
    """
    # Создание поддельного пользователя с пустой электронной почтой
    mock_user = UserModel(email="")

    with pytest.raises(HTTPException) as exc_info:
        await get_current_username(mock_user)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    await create_tables()

@pytest.mark.asyncio
async def test_add_user():
    """
        Тестирует успешную регистрацию нового пользователя через API.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/auth/signup",
            json={
                "name": "Ванюша",
                "email": "van@exmpjl.com",
                "password": "pass"
            }
        )
    assert response.status_code == 201
    assert response.json() == {"success": True, "message": "Регистрация прошла успешно"}



client_1 = TestClient(app)
fake = faker.Faker()

client_1.fake_user_email = fake.email()
client_1.fake_user_password = fake.password()
client_1.fake_user_name = fake.first_name()
client_1.new_user_id = 0
client_1.auth_token = ""

def test_signup():
    """
        Тестирует процесс регистрации нового пользователя
        с использованием фейковых данных.
    """
    response = client_1.post("/auth/signup",
                           json={"email": client_1.fake_user_email,
                                 "password": client_1.fake_user_password,
                                 "name": client_1.fake_user_name}
    )
    assert response.status_code == 201
    client_1.new_user_id = response.json()


def test_login():
    """
        Тестирует процесс входа пользователя
        с использованием фейковых данных.
    """
    response = client_1.post("/auth/login",
                           data={"username": client_1.fake_user_email,
                                 "password": client_1.fake_user_password}
    )
    assert response.status_code == 200
    client_1.auth_token = response.json()['access_token']
