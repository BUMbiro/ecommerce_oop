"""
Тесты для классов Product и Category.
"""

import json
import tempfile
import os
from src.products import Product, Category, load_products_from_json


def test_product_initialization() -> None:
    """Проверяет инициализацию объекта Product."""
    p = Product("Ноутбук", "Игровой ноутбук", 1500.50, 10)
    assert p.name == "Ноутбук"
    assert p.description == "Игровой ноутбук"
    assert p.price == 1500.50
    assert p.quantity == 10


def test_category_initialization() -> None:
    """Проверяет инициализацию объекта Category."""
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Разные гаджеты", [p1, p2])
    assert cat.name == "Электроника"
    assert cat.description == "Разные гаджеты"
    assert len(cat.products) == 2
    assert cat.products[0] is p1


def test_category_counters() -> None:
    """Проверяет автоматическое обновление счётчиков category_count и product_count."""
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Товар1", "Описание1", 10, 5)
    p2 = Product("Товар2", "Описание2", 20, 3)

    Category("Кат1", "Описание кат1", [p1])
    assert Category.category_count == 1
    assert Category.product_count == 1

    Category("Кат2", "Описание кат2", [p2, p1])
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_load_products_from_json() -> None:
    """Проверяет загрузку данных из JSON-файла."""
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание категории",
            "products": [
                {
                    "name": "Тестовый товар",
                    "description": "Описание товара",
                    "price": 100.0,
                    "quantity": 10
                }
            ]
        }
    ]

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.json', delete=False, encoding='utf-8'
    ) as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_path = f.name

    try:
        categories = load_products_from_json(temp_path)
        assert len(categories) == 1
        assert categories[0].name == "Тестовая категория"
        assert len(categories[0].products) == 1
        assert categories[0].products[0].name == "Тестовый товар"
        assert categories[0].products[0].price == 100.0
    finally:
        os.unlink(temp_path)
