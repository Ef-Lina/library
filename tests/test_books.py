"""
Модуль тестирования обработки книг и аннотаций.

Этот модуль предоставляет функциональность
для  тестирования управления книгами и их аннотациями.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from src.main import app
from src.models.books import BookModel
from src.repository import BookRepository
from src.schemas.annotation import AnnotateSchema
from src.models.annotation import AnnotateModel
from src.database import new_session
from src.database import delete_tables

@pytest.mark.asyncio
async def test_get_books_start():
    """Тест получения списка книг."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books_1/")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_add_book():
    """Тест добавления книги."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/books_1/", json={"title": "To Kill a Mockingbird",
                               "author": "Harper Lee",
                               "year": 1960,
                               "pages": 120}
        )
    assert response.status_code == 201
    assert response.json() == {"success": True, "message": "Книга успешно добавлена"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/books_1/", json={"title": "To Kill a Mockingbird",
                               "author": "Harper Lee",
                               "year": 1960,
                               "pages": 120}
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "Книга с таким названием уже существует."}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/books_1/",
            json={"title": "1984",
                  "author": "George Orwel",
                  "year": 1949,
                  "pages": 100}
        )
    assert response.status_code == 201
    assert response.json() == {"success": True, "message": "Книга успешно добавлена"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/books_1/",
            json={"author": "George Orwel",
                  "year": 1949,
                  "pages": 100}
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_books():
    """Тест получения списка книг."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books_1/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Проверяем, что возвращается список
    data = response.json()
    assert len(data) == 2
    assert data [0] ["id"] == 1
    assert data [0]["title"] == "To Kill a Mockingbird"
    assert data [0]["author"] == "Harper Lee"
    assert data [0]["year"] == 1960
    assert data [0]["pages"] == 120
    assert data[1]["id"] == 2
    assert data[1]["title"] == "1984"
    assert data[1]["author"] == "George Orwel"
    assert data[1]["year"] == 1949
    assert data[1]["pages"] == 100


@pytest.mark.asyncio
async def test_get_book_by_id():
    """Тест получения книги по ID."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books_1/1")  # Предполагаем, что книга с ID 1 существует
    assert response.status_code == 200
    assert response.json()["title"] == "To Kill a Mockingbird"  # Проверьте название книги
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books_1/3")  # Предполагаем, что книга с ID 3 не существует
    assert response.status_code == 404
    assert response.json() == {"detail": "Книга не найдена"}


@pytest.mark.asyncio
async def test_update_book_by_id():
    """Тест обновления книги по ID."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/books_1/2",
            json={"title": "Animal Farm",
                  "author": "George Orwel",
                  "year": 1945,
                  "pages": 111}
        )
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Данные книги успешно обновлены"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/books_1/5",
            json={"title": "Farm",
                  "author": "George Orwel",
                  "year": 1944,
                  "pages": 101}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": "Книга не найдена"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/books_1/2",
            json={"title": "Farm",
                  "author": "George Orwel",
                  "year": 1944,
                  "pages": "good"}
        )
    assert response.status_code == 422
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch(
            "/books_1/2",
            json={"title": "Farm",
                  "author": "George Orwel",
                  "year": "go",
                  "pages": 100}
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_book_by_id():
    """Тест удаления книги по ID."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/books_1/1")  # Удаляем книгу с ID 1
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Книга успешно удалена"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/books_1/1")  # Удаляем книгу с ID 1
    assert response.status_code == 404
    assert response.json() == {"detail": "Книга не найдена"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/books_1/2")  # Удаляем книгу с ID 2
    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "Книга успешно удалена"}


@pytest.fixture
async def setup_database():
    """Фикстура для настройки базы данных перед тестами."""
    async with new_session() as session:
        # Очистите базу данных перед тестом
        await session.execute(select(BookModel).delete())
        await session.execute(select(AnnotateModel).delete())
        await session.commit()

        yield session  # Возвращаем сессию для использования в тестах

        # Очистите базу данных после теста
        await session.execute(select(BookModel).delete())
        await session.execute(select(AnnotateModel).delete())
        await session.commit()


@pytest.mark.asyncio
async def test_add_one(setup_database):
    """Тест добавления одной аннотации."""
    data = AnnotateSchema(title="Test Book", annotation="This is a test annotation.")

    annotation_id = await BookRepository.add_one(data)

    async with new_session() as session:
        result = await session.execute(select(AnnotateModel).filter_by(annotation_id=annotation_id))
        annotation = result.scalar_one_or_none()

        assert annotation is not None
        assert annotation.annotation == "This is a test annotation."


@pytest.mark.asyncio
async def test_find_all(setup_database):
    """Тест поиска всех книг с аннотациями."""
    book1 = BookModel(title="Test Book 1",
                      author="Author A",
                      year=2021,
                      pages=100)  # Укажите количество страниц
    book2 = BookModel(title="Test Book 2",
                      author="Author B",
                      year=2022,
                      pages=200)  # Укажите количество страниц

    async with new_session() as session:
        session.add(book1)
        session.add(book2)
        await session.commit()

    data1 = AnnotateSchema(title="Test Book 1",
                           annotation="Annotation for Test Book 1.")
    data2 = AnnotateSchema(title="Test Book 2",
                           annotation="Annotation for Test Book 2.")

    await BookRepository.add_one(data1)
    await BookRepository.add_one(data2)

    books_with_annotations = await BookRepository.find_all()

    assert len(books_with_annotations) == 2

    assert books_with_annotations[0]["title"] == "Test Book 1"
    assert books_with_annotations[0]["annotation"] == "Annotation for Test Book 1."

    assert books_with_annotations[1]["title"] == "Test Book 2"
    assert books_with_annotations[1]["annotation"] == "Annotation for Test Book 2."


@pytest.mark.asyncio
async def test_add_annotation():
    """Тест добавления аннотации напрямую."""
    sample_annotation = {
           "title": "Sample Book",
           "annotation": "This is a sample annotation."
       }
    result = await BookRepository.add_one(AnnotateSchema(**sample_annotation))
    assert result is not None  # Проверка успешного добавления
    await delete_tables()
