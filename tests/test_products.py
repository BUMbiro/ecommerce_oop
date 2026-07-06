"""
Тесты для классов Product, Category, CategoryIterator, Smartphone, LawnGrass.
"""

import json
import tempfile
import os
import pytest
from src.products import Product, Category, CategoryIterator, Smartphone, LawnGrass, load_products_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


# ---------- Старые тесты (без изменений) ----------

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
    assert p.price == 2000.0


def test_category_initialization() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Разные гаджеты", [p1, p2])
    assert cat.name == "Электроника"
    assert "Мышь" in cat.products
    assert "Клавиатура" in cat.products


def test_category_add_product() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    cat = Category("Электроника", "Гаджеты", [p1])
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat.add_product(p2)
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
    assert p1 + p2 == 1400


def test_product_add_type_error() -> None:
    p1 = Product("Товар А", "Описание", 100, 10)
    with pytest.raises(TypeError, match="Складывать можно только объекты Product"):
        p1 + 100


def test_category_iterator() -> None:
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    iterator = CategoryIterator(cat)
    products_from_iter = list(iterator)
    assert products_from_iter == [p1, p2]
    products_from_for = []
    for product in cat:
        products_from_for.append(product)
    assert products_from_for == [p1, p2]
    it = iter(cat)
    next(it)
    next(it)
    with pytest.raises(StopIteration):
        next(it)


def test_category_iterator_empty_category() -> None:
    cat = Category("Пустая", "Без товаров", [])
    iterator = CategoryIterator(cat)
    assert list(iterator) == []
    for _ in cat:
        assert False


# ---------- Новые тесты для классов-наследников (исправлены типы) ----------

def test_smartphone_creation() -> None:
    phone = Smartphone("Samsung", "Флагман", 1000.0, 5,
                       95.5, "S23", 256, "Черный")  # efficiency — float
    assert phone.name == "Samsung"
    assert phone.price == 1000.0
    assert phone.quantity == 5
    assert phone.efficiency == 95.5
    assert phone.model == "S23"
    assert phone.memory == 256
    assert phone.color == "Черный"
    assert isinstance(phone, Product)


def test_lawn_grass_creation() -> None:
    grass = LawnGrass("Газон", "Спорт", 50.0, 100,
                      "Россия", "14 дней", "Зелёный")  # germination_period — строка
    assert grass.name == "Газон"
    assert grass.price == 50.0
    assert grass.quantity == 100
    assert grass.country == "Россия"
    assert grass.germination_period == "14 дней"
    assert grass.color == "Зелёный"
    assert isinstance(grass, Product)


def test_add_same_class_products_works() -> None:
    p1 = Product("Товар А", "", 100, 10)
    p2 = Product("Товар Б", "", 200, 2)
    assert p1 + p2 == 1400

    phone1 = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")
    phone2 = Smartphone("Apple", "", 1200, 3, 98.2, "15", 512, "Серебро")
    assert phone1 + phone2 == 1000 * 5 + 1200 * 3  # 8600


def test_add_different_classes_raises_type_error() -> None:
    phone = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")
    grass = LawnGrass("Газон", "", 50, 100, "Россия", "14 дней", "Зелёный")
    with pytest.raises(TypeError, match="Нельзя складывать Smartphone и LawnGrass"):
        phone + grass

    product = Product("Ноутбук", "", 1500, 3)
    with pytest.raises(TypeError, match="Нельзя складывать Product и Smartphone"):
        product + phone


def test_add_product_to_category_with_wrong_type_raises() -> None:
    cat = Category("Тест", "Описание", [])
    with pytest.raises(TypeError, match="можно добавлять только объекты Product"):
        cat.add_product("not a product")
    with pytest.raises(TypeError, match="можно добавлять только объекты Product"):
        cat.add_product(123)
    # Но можно добавить наследника
    phone = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")
    cat.add_product(phone)
    assert Category.product_count == 1
    assert "Samsung" in cat.products
