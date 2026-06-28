"""
Тесты для классов Product, Category и CategoryIterator.
"""

import json
import tempfile
import os
import pytest
from src.products import Product, Category, CategoryIterator, load_products_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Автоматически сбрасывает счётчики категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_initialization() -> None:
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    assert p.name == "Ноутбук"
    assert p.price == 1500.50
    assert p.quantity == 10


def test_product_price_setter() -> None:
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    p.price = 2000.0
    assert p.price == 2000.0

    p.price = -100.0
    assert p.price == 2000.0  # цена не изменилась


def test_category_initialization() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Разные гаджеты", [p1, p2])
    assert cat.name == "Электроника"
    # Проверяем через геттер (не обращаемся к приватному атрибуту)
    assert "Мышь" in cat.products
    assert "Клавиатура" in cat.products


def test_category_add_product() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    cat = Category("Электроника", "Гаджеты", [p1])
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat.add_product(p2)
    # Проверяем через геттер
    assert "Мышь" in cat.products
    assert "Клавиатура" in cat.products
    assert Category.product_count == 2


def test_category_products_property() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    expected = "Мышь, 25.0 руб. Остаток: 50 шт.\nКлавиатура, 80.0 руб. Остаток: 20 шт.\n"
    assert cat.products == expected


def test_product_classmethod_new_product() -> None:
    data = {"name": "Смартфон", "description": "AMOLED", "price": 500.0, "quantity": 10}
    p = Product.new_product(data)
    assert p.name == "Смартфон"
    assert p.price == 500.0
    assert p.quantity == 10


def test_product_classmethod_new_product_duplicate() -> None:
    existing = Product("Смартфон", "AMOLED", 500.0, 10)
    data = {"name": "Смартфон", "description": "AMOLED", "price": 600.0, "quantity": 5}
    p = Product.new_product(data, [existing])
    assert p is existing
    assert p.quantity == 15
    assert p.price == 600.0


def test_load_products_from_json() -> None:
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание категории",
            "products": [
                {"name": "Тестовый товар", "description": "Описание товара", "price": 100.0, "quantity": 10}
            ]
        }
    ]
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_path = f.name

    try:
        categories = load_products_from_json(temp_path)
        assert len(categories) == 1
        assert categories[0].name == "Тестовая категория"
        expected = "Тестовый товар, 100.0 руб. Остаток: 10 шт.\n"
        assert categories[0].products == expected
    finally:
        os.unlink(temp_path)


# ---------- Новые тесты для магических методов ----------

def test_product_str() -> None:
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    assert str(p) == "Ноутбук, 1500.5 руб. Остаток: 10 шт."


def test_category_str() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    assert str(cat) == "Электроника, количество продуктов: 70 шт."


def test_product_add() -> None:
    p1 = Product("Товар А", "Описание", 100, 10)
    p2 = Product("Товар Б", "Описание", 200, 2)
    assert p1 + p2 == 100 * 10 + 200 * 2  # 1400


def test_product_add_type_error() -> None:
    p1 = Product("Товар А", "Описание", 100, 10)
    with pytest.raises(TypeError, match="Складывать можно только объекты Product"):
        p1 + 100  # передаём int, mypy не ругается, т.к. сигнатура (object)


# ---------- Тесты для итератора (доп. задание) ----------

def test_category_iterator() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])

    # Проверяем явное использование CategoryIterator
    iterator = CategoryIterator(cat)
    products_from_iter = list(iterator)
    assert products_from_iter == [p1, p2]

    # Проверяем, что можно итерировать напрямую через __iter__ в Category
    products_from_for = []
    for product in cat:
        products_from_for.append(product)
    assert products_from_for == [p1, p2]

    # Проверяем, что итератор поднимает StopIteration корректно
    it = iter(cat)
    next(it)  # p1
    next(it)  # p2
    with pytest.raises(StopIteration):
        next(it)


def test_category_iterator_empty_category() -> None:
    cat = Category("Пустая", "Без товаров", [])
    # Явный итератор
    iterator = CategoryIterator(cat)
    assert list(iterator) == []
    # Цикл for
    for _ in cat:
        assert False, "Цикл не должен выполняться"
