"""
Тесты для всех классов: Product, Category, Smartphone, LawnGrass, BaseProduct, Order.
"""
import inspect
import json
import tempfile
import os
import pytest
from src.products import (
    Product,
    Category,
    CategoryIterator,
    Smartphone,
    LawnGrass,
    BaseProduct,
    Order,
    BaseModel,
    load_products_from_json,
)


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield


# ---------- Старые тесты ----------
def test_product_initialization():
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    assert p.name == "Ноутбук"
    assert p.price == 1500.50
    assert p.quantity == 10


def test_product_price_setter():
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    p.price = 2000.0
    assert p.price == 2000.0
    p.price = -100.0
    assert p.price == 2000.0


def test_category_initialization():
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Разные гаджеты", [p1, p2])
    assert cat.name == "Электроника"
    assert "Мышь" in cat.products
    assert "Клавиатура" in cat.products


def test_category_add_product():
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    cat = Category("Электроника", "Гаджеты", [p1])
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat.add_product(p2)
    assert "Мышь" in cat.products
    assert "Клавиатура" in cat.products
    assert Category.product_count == 2


def test_category_products_property():
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    expected = "Мышь, 25.0 руб. Остаток: 50 шт.\nКлавиатура, 80.0 руб. Остаток: 20 шт.\n"
    assert cat.products == expected


def test_product_classmethod_new_product():
    data = {"name": "Смартфон", "description": "AMOLED", "price": 500.0, "quantity": 10}
    p = Product.new_product(data)
    assert p.name == "Смартфон"
    assert p.price == 500.0
    assert p.quantity == 10


def test_product_classmethod_new_product_duplicate():
    existing = Product("Смартфон", "AMOLED", 500.0, 10)
    data = {"name": "Смартфон", "description": "AMOLED", "price": 600.0, "quantity": 5}
    p = Product.new_product(data, [existing])
    assert p is existing
    assert p.quantity == 15
    assert p.price == 600.0


def test_load_products_from_json():
    test_data = [
        {
            "name": "Тестовая категория",
            "description": "Описание",
            "products": [
                {"name": "Товар", "description": "Описание", "price": 100.0, "quantity": 10}
            ],
        }
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_path = f.name
    try:
        categories = load_products_from_json(temp_path)
        assert len(categories) == 1
        assert categories[0].name == "Тестовая категория"
        expected = "Товар, 100.0 руб. Остаток: 10 шт.\n"
        assert categories[0].products == expected
    finally:
        os.unlink(temp_path)


def test_product_str():
    p = Product("Ноутбук", "Игровой", 1500.50, 10)
    assert str(p) == "Ноутбук, 1500.5 руб. Остаток: 10 шт."


def test_category_str():
    p1 = Product("Мышь", "Беспроводная", 25.0, 50)
    p2 = Product("Клавиатура", "Механическая", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    assert str(cat) == "Электроника, количество продуктов: 70 шт."


def test_product_add():
    p1 = Product("А", "", 100, 10)
    p2 = Product("Б", "", 200, 2)
    assert p1 + p2 == 1400


def test_product_add_type_error():
    p = Product("А", "", 100, 10)
    with pytest.raises(TypeError, match="Складывать можно только объекты Product"):
        p + 100


def test_category_iterator():
    p1 = Product("Мышь", "", 25.0, 50)
    p2 = Product("Клавиатура", "", 80.0, 20)
    cat = Category("Электроника", "Гаджеты", [p1, p2])
    it = CategoryIterator(cat)
    assert list(it) == [p1, p2]
    assert [p for p in cat] == [p1, p2]


def test_category_iterator_empty():
    cat = Category("Пустая", "", [])
    it = CategoryIterator(cat)
    assert list(it) == []


# ---------- Тесты для наследников (из прошлой домашки) ----------
def test_smartphone_creation():
    phone = Smartphone("Samsung", "Флагман", 1000.0, 5, 95.5, "S23", 256, "Черный")
    assert phone.efficiency == 95.5
    assert phone.model == "S23"
    assert phone.memory == 256
    assert phone.color == "Черный"
    assert isinstance(phone, Product)


def test_lawn_grass_creation():
    grass = LawnGrass("Газон", "Спорт", 50.0, 100, "Россия", "14 дней", "Зелёный")
    assert grass.country == "Россия"
    assert grass.germination_period == "14 дней"
    assert grass.color == "Зелёный"
    assert isinstance(grass, Product)


def test_add_different_classes_raises():
    phone = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")
    grass = LawnGrass("Газон", "", 50, 100, "Россия", "14 дней", "Зелёный")
    with pytest.raises(TypeError, match="Нельзя складывать Smartphone и LawnGrass"):
        phone + grass


def test_add_product_to_category_wrong_type():
    cat = Category("Тест", "", [])
    with pytest.raises(TypeError, match="можно добавлять только объекты Product"):
        cat.add_product("not a product")
    with pytest.raises(TypeError, match="можно добавлять только объекты Product"):
        cat.add_product(123)


# ---------- Новые тесты для абстрактного класса и миксина ----------

def test_abstract_base_product_cannot_instantiate():
    assert inspect.isabstract(BaseProduct) is True


def test_product_inherits_base_product():
    assert issubclass(Product, BaseProduct)


def test_log_mixin_output(capsys):
    # Создаём объекты, чтобы проверить вывод – используем их в assert
    p = Product("Тест", "Описание", 100, 5)
    captured = capsys.readouterr()
    assert "Product('Тест', 'Описание', 100, 5)" in captured.out

    s = Smartphone("Samsung", "Флагман", 1000, 5, 95.5, "S23", 256, "Черный")
    captured = capsys.readouterr()
    assert (
        "Smartphone('Samsung', 'Флагман', 1000, 5, 95.5, 'S23', 256, 'Черный')"
        in captured.out
    )

    # Чтобы убрать warning о неиспользуемых переменных – используем их
    assert p.name == "Тест"
    assert s.model == "S23"


# ---------- Тесты для Order (доп. задание) ----------
def test_order_creation():
    p = Product("Ноутбук", "Игровой", 1500, 2)
    order = Order(p, 3)
    assert order.total_price == 4500
    assert order.name == "Заказ на Ноутбук"
    assert "Ноутбук" in order.description
    assert isinstance(order, BaseModel)


def test_category_inherits_base_model():
    assert issubclass(Category, BaseModel)
    cat = Category("Электроника", "Описание", [])
    assert isinstance(cat, BaseModel)
