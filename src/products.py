"""
Модуль с классами Product и Category для интернет-магазина.
Реализована инкапсуляция: приватные атрибуты, геттеры, сеттеры, класс-метод.
"""

import json
from typing import List, Optional


class Product:
    """Товар интернет-магазина."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price          # приватный атрибут с двойным подчёркиванием
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены (возвращает значение приватного атрибута)."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """
        Сеттер для цены с проверкой на положительность.
        Если цена <= 0, выводится сообщение и цена не меняется.
        """
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[List['Product']] = None) -> 'Product':
        """
        Класс-метод для создания продукта из словаря.
        Если передан список existing_products, проверяет дубликаты по имени:
        - если дубликат найден, складывает количество и выбирает максимальную цену.
        """
        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

        # Дополнительное задание: проверка дубликатов
        if existing_products is not None:
            for existing in existing_products:
                if existing.name.lower() == name.lower():
                    # Складываем количество
                    existing.quantity += quantity
                    # Выбираем максимальную цену (через сеттер)
                    if price > existing.price:
                        existing.price = price
                    return existing

        # Если дубликата нет, создаём новый продукт
        return cls(name, description, price, quantity)


class Category:
    """Категория товаров."""
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self._products = products          # приватный атрибут (одно подчёркивание — защищённый)

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """
        Добавляет продукт в категорию и обновляет общий счётчик товаров.
        """
        self._products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер для списка продуктов. Возвращает строку с продуктами в формате:
        "Название продукта, X руб. Остаток: X шт.\n"
        """
        result = ""
        for p in self._products:
            result += f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n"
        return result


def load_products_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON-файла, создаёт объекты.
    Если файл не найден, возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    categories = []
    all_products: List[Product] = []   # для проверки дубликатов

    for cat_data in data:
        products = []
        for product_data in cat_data.get('products', []):
            # Используем класс-метод для создания продукта с учётом дубликатов
            product = Product.new_product(product_data, all_products)
            # Если продукт новый — добавляем в текущую категорию и в общий список
            if product not in products and product not in all_products:
                products.append(product)
                all_products.append(product)
        category = Category(cat_data['name'], cat_data['description'], products)
        categories.append(category)
    return categories
