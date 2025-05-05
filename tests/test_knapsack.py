"""
Модуль оптимизации - решение задачи о рюкзаке.

Этот модуль содержит реализацию алгоритма для решения задачи о рюкзаке,
где необходимо выбрать набор предметов с заданными весами и ценностями так,
чтобы максимизировать общую ценность, не превышая заданную вместимость рюкзака.

Функции:
- knapsack(weights: List[int], values: List[int], capacity: int) -> Tuple[int, int, List[int]]:
    Решает задачу о рюкзаке и возвращает максимальную ценность, количество
    выбранных предметов и индексы выбранных предметов.
"""
from src.api.optimization import knapsack



def test_knapsack_basic():
    """
        Тест для базового случая задачи о рюкзаке.

        Проверяет, что функция корректно выбирает все доступные предметы,
        чтобы максимизировать общую ценность.
    """
    weights = [1, 2, 3]
    values = [10, 15, 40]
    capacity = 6
    expected = (65, 3, [0, 1, 2])  # Total value, item count, selected items (indices)
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_partial_selection():
    """
       Тест для случая частичного выбора предметов.

       Проверяет, что функция правильно выбирает предметы при ограниченной
       вместимости рюкзака.
    """
    weights = [2, 3, 4]
    values = [40, 50, 60]
    capacity = 5
    expected = (90, 2, [0, 1])  # Total value, item count, selected items (indices)
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_empty():
    """
        Тест для случая пустого рюкзака.

        Проверяет поведение функции при отсутствии предметов.
    """
    weights = []
    values = []
    capacity = 5
    expected = (0, 0, [])  # Total value, item count, selected items (no items)
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_exceeding_capacity():
    """
        Тест для случая превышения вместимости.

        Проверяет поведение функции при невозможности выбрать ни один предмет
        из-за недостаточной вместимости.
    """
    weights = [8, 10, 12]
    values = [10, 20, 30]
    capacity = 5
    expected = (0, 0, [])  # No items can be selected, capacity too small
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_all_items_fit():
    """
        Тест для случая, когда все предметы помещаются в рюкзак.

        Проверяет правильность выбора всех доступных предметов.
    """
    weights = [1, 2, 3]
    values = [10, 20, 30]
    capacity = 6
    expected = (60, 3, [0, 1, 2])  # Can take all items
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_single_item():
    """
        Тест для случая с одним предметом.

        Проверяет выбор единственного предмета при точном совпадении
        его веса с вместимостью рюкзака.
    """
    weights = [5]
    values = [10]
    capacity = 5
    expected = (10, 1, [0])  # Fit exactly one item
    assert knapsack(weights, values, capacity) == expected


def test_knapsack_multiple_optimal_solutions():
    """
        Тест для случая с несколькими оптимальными решениями.

        Проверяет правильность выбора при наличии нескольких вариантов
        с одинаковой максимальной ценностью.
    """
    weights = [1, 2, 5]
    values = [10, 12, 15]
    capacity = 5
    expected = (22, 2, [0, 1])  # Best choice here is to select item 1 and 0
    assert knapsack(weights, values, capacity) == expected
