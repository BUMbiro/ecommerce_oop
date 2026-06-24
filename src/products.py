"""
Модуль с классами Product и Category для интернет-магазина.
"""

import json
from typing import List


class Product:
    """Товар интернет-магазина."""
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Категория товаров."""
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


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
    for cat_data in data:
        products = []
        for product_data in cat_data.get('products', []):
            product_item = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )
            products.append(product_item)
        category = Category(
            name=cat_data['name'],
            description=cat_data['description'],
            products=products
        )
        categories.append(category)
    return categories
