"""
Тесты для классов Product и Category.
"""

import json
import tempfile
import os
import pytest
from src.products import Product, Category, load_products_from_json


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
