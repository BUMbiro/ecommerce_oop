"""
Модуль с классами Product и Category для интернет-магазина.
Теперь с приватными атрибутами, геттерами, сеттерами и класс-методами.
"""

import json
from typing import List, Optional


class Product:
    """Товар интернет-магазина."""
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self._price = price          # приватная цена
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой на положительность."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self._price = new_price

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

        # Проверка дубликатов (доп. задание)
        if existing_products is not None:
            for existing in existing_products:
                if existing.name.lower() == name.lower():
                    # Складываем количество
                    existing.quantity += quantity
                    # Выбираем максимальную цену
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
        self._products = products  # теперь приватный

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет продукт в категорию и обновляет счётчик."""
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
    all_products: List[Product] = []  # для проверки дубликатов при создании (доп. задание)

    for cat_data in data:
        products = []
        for product_data in cat_data.get('products', []):
            # Используем класс-метод new_product для создания продуктов с учётом дубликатов
            # Передаём список всех уже созданных продуктов для проверки
            product = Product.new_product(product_data, all_products)
            # Если продукт уже существовал, он не будет добавлен повторно, но мы должны учесть это.
            # Для простоты будем добавлять только если продукт новый (его нет в all_products)
            if product not in products and product not in all_products:
                products.append(product)
                all_products.append(product)
            # Если продукт уже был в all_products, он уже добавлен, но quantity и price обновлены через new_product
            # В этом случае мы не добавляем его повторно, чтобы избежать дублирования в списке.
        category = Category(cat_data['name'], cat_data['description'], products)
        categories.append(category)
    return categories
