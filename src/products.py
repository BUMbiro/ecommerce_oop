"""
Модуль с классами Product, Category, CategoryIterator, Smartphone, LawnGrass.
Реализована инкапсуляция, магические методы, наследование, проверка типов.
"""

import json
from typing import List, Optional


class Product:
    """Базовый класс для товаров интернет-магазина."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[List['Product']] = None) -> 'Product':
        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']

        if existing_products is not None:
            for existing in existing_products:
                if existing.name.lower() == name.lower():
                    existing.quantity += quantity
                    if price > existing.price:
                        existing.price = price
                    return existing

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        """
        Сложение товаров только если они одного класса.
        Проверка через type().
        """
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты Product и его наследников")
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать {type(self).__name__} и {type(other).__name__}")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс Смартфон — наследник Product."""
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс Трава газонная — наследник Product."""
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Категория товаров."""
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: object) -> None:
        """
        Добавляет продукт в категорию.
        Проверка через isinstance(), что добавляется только Product или наследник.
        """
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products) + ("\n" if self.__products else "")

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def get_products(self) -> List[Product]:
        return self.__products

    def __iter__(self):
        return CategoryIterator(self)


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: Category):
        self._category = category
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        products = self._category.get_products()
        if self._index < len(products):
            product = products[self._index]
            self._index += 1
            return product
        raise StopIteration


def load_products_from_json(file_path: str) -> List[Category]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []

    categories = []
    all_products: List[Product] = []

    for cat_data in data:
        products = []
        for product_data in cat_data.get('products', []):
            product = Product.new_product(product_data, all_products)
            if product not in products and product not in all_products:
                products.append(product)
                all_products.append(product)
        category = Category(cat_data['name'], cat_data['description'], products)
        categories.append(category)
    return categories
