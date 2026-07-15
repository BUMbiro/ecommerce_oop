"""
Модуль с классами: абстрактный BaseProduct, миксин LogMixin,
Product, Smartphone, LawnGrass, Category, CategoryIterator, Order (доп.).
Добавлены: проверка нулевого количества, метод average_price, пользовательское исключение ZeroQuantityError.
"""
import json
from abc import ABC, abstractmethod
from typing import List, Optional


# ---------- Абстрактный базовый класс для продуктов ----------
class BaseProduct(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @property
    @abstractmethod
    def quantity(self) -> int:
        pass


# ---------- Миксин для логирования создания ----------
class LogMixin:
    def __init__(self, *args, **kwargs):
        print(repr(self))


# ---------- Пользовательское исключение (доп. задание) ----------
class ZeroQuantityError(Exception):
    """Исключение для случая, когда товар имеет нулевое количество."""
    pass


# ---------- Базовый класс Product ----------
class Product(BaseProduct, LogMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self._name = name
        self._description = description
        self.__price = price
        self._quantity = quantity
        super().__init__()

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = new_price

    @property
    def quantity(self) -> int:
        return self._quantity

    @classmethod
    def new_product(cls, product_data: dict, existing_products: Optional[List['Product']] = None) -> 'Product':
        name = product_data['name']
        description = product_data['description']
        price = product_data['price']
        quantity = product_data['quantity']
        # Проверка количества при создании через new_product
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        if existing_products is not None:
            for existing in existing_products:
                if existing.name.lower() == name.lower():
                    existing._quantity += quantity
                    if price > existing.price:
                        existing.price = price
                    return existing
        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты Product и его наследников")
        if type(self) is not type(other):
            raise TypeError(f"Нельзя складывать {type(self).__name__} и {type(other).__name__}")
        return self.price * self.quantity + other.price * other.quantity

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"{self._name!r}, {self._description!r}, {self.price}, {self.quantity})")


# ---------- Наследники Product ----------
class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"{self._name!r}, {self._description!r}, {self.price}, {self.quantity}, "
                f"{self.efficiency}, {self.model!r}, {self.memory}, {self.color!r})")


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"{self._name!r}, {self._description!r}, {self.price}, {self.quantity}, "
                f"{self.country!r}, {self.germination_period!r}, {self.color!r})")


# ---------- Абстрактный базовый класс для Category и Order ----------
class BaseModel(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass


# ---------- Категория ----------
class Category(BaseModel):
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self._name = name
        self._description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    def add_product(self, product: object) -> None:
        """Добавляет продукт в категорию. Проверяет тип и количество (доп. задание)."""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты Product или его наследников")
        try:
            if product.quantity == 0:
                raise ZeroQuantityError("Товар с нулевым количеством не может быть добавлен")
            self.__products.append(product)
            Category.product_count += 1
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
        else:
            print("Товар добавлен")
        finally:
            print("Обработка добавления товара завершена")

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

    def middle_price(self) -> float:
        """Возвращает среднюю цену всех товаров в категории. Если товаров нет – возвращает 0."""
        try:
            total = sum(p.price for p in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0.0


class CategoryIterator:
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


# ---------- Заказ (доп. задание) ----------
class Order(BaseModel):
    def __init__(self, product: Product, quantity: int):
        try:
            if product.quantity == 0:
                raise ZeroQuantityError("Товар с нулевым количеством не может быть в заказе")
            self._product = product
            self._quantity = quantity
            self._total_price = product.price * quantity
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            # Не создаём заказ, но можно установить пустые атрибуты или оставить без
            # В else мы не попадём, поэтому заказ не создаётся.
        else:
            print("Заказ создан")
        finally:
            print("Обработка создания заказа завершена")

    @property
    def name(self) -> str:
        return f"Заказ на {self._product.name}" if hasattr(self, '_product') else "Заказ не создан"

    @property
    def description(self) -> str:
        if hasattr(self, '_product'):
            return f"Товар: {self._product.name}, количество: {self._quantity}, итого: {self._total_price} руб."
        return "Заказ не создан из-за ошибки"

    @property
    def product(self) -> Optional[Product]:
        return getattr(self, '_product', None)

    @property
    def quantity(self) -> int:
        return getattr(self, '_quantity', 0)

    @property
    def total_price(self) -> float:
        return getattr(self, '_total_price', 0.0)

    def __str__(self) -> str:
        if hasattr(self, '_product'):
            return f"Заказ: {self._product.name}, {self._quantity} шт., итого {self._total_price} руб."
        return "Заказ не создан"


# ---------- Загрузка из JSON ----------
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
