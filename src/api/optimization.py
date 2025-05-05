"""Модуль для определения оптимальной подборки книг."""
from fastapi import status, HTTPException, APIRouter
from sqlalchemy import select
from src.api.dependencies import SessionDep
from src.models.books import BookModel

router = APIRouter(tags=["Оптимальная подборка книг для чтения 🧮"])




@router.get("/opt", summary="Возможные книги",
            status_code=status.HTTP_200_OK)
async def get_optimal_result(session: SessionDep,
                             days: int, pages: int):
    """
    Эндпоинт для получения максимального
    количества книг и их названий из базы данных
    которые можно прочитать за задонные дни при
    заданном количестве страниц в день.
    """
    max_value, items_count, titles = await show_result(days,
                                                  pages, session)
    if not max_value:
        return {"massage": "Нет вариантов"}
    return {"items_count": items_count, "titles": titles}

def knapsack(weights, values, capacity):
    """Функция для решения задачи о рюкзаке."""
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Заполнение таблицы dp
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w -
                                         weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    max_value = dp[n][capacity]
    w = capacity
    items_count = 0
    selected_items = []

    # Обратное извлечение выбранных предметов
    for i in range(n, 0, -1):
        if max_value != dp[i - 1][w]:  # Проверка на
                                        # изменение значения
            selected_items.append(i - 1)  # Индекс предмета
            items_count += 1
            w -= weights[i - 1]  # Уменьшение оставшейся емкости
            max_value -= values[i - 1]  # Обновление
                                    # max_value для следующей итерации

    selected_items.reverse()  # Чтобы вернуть индексы в порядке выбора
    return dp[n][capacity], items_count, selected_items



async def show_pages_years(session: SessionDep):
    """Получает список страниц и годов публикации
     книг из базы данных."""
    query = select(BookModel)
    result = await session.execute(query)
    books = result.scalars().all()

    if not books:
        raise HTTPException(status_code=status
                            .HTTP_204_NO_CONTENT,
                            detail="Библиотека пуста")

    pages_list = [book.pages for book in books]
    years_list = [book.year for book in books]
    titles_list = [book.title for book in books]

    return pages_list, years_list, titles_list


async def show_result(days, pages_per_day, session: SessionDep):
    """Вычисляет максимальное количество книг,
    которые можно прочитать за заданное время."""
    capacity = days * pages_per_day
    pages_list, years_list, titles_list = await show_pages_years(session)
    max_value, items_count, selected_items = knapsack(
        pages_list, years_list, capacity)
    titles = [titles_list[x] for x in selected_items]
    return max_value, items_count, titles
