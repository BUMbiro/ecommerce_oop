# 🛍️ ООП-модель интернет-магазина

Привет! Это учебный проект, в котором я на практике разбираюсь с объектно-ориентированным программированием (ООП) 
на **Python**. Здесь нет сложного бэкенда или базы данных — только классы, которые описывают товары, 
категории и заказы для интернет-магазина.

Проект прошёл путь от простых классов до абстракций, миксинов, итераторов и проверок типов. Код покрыт тестами (93%),
соответствует **PEP8** и проверен mypy.

---

## 🎯 Что умеет этот проект?

- **Создавать товары** (`Product`), смартфоны (`Smartphone`) и газонную траву (`LawnGrass`).
- **Группировать товары в категории** (`Category`) с автоматическим подсчётом количества.
- **Защищать данные** — приватные атрибуты, геттеры, сеттеры.
- **Выводить информацию** через `__str__` и `__repr__`.
- **Складывать товары** (`__add__`) только одного класса (проверка через `type()`).
- **Перебирать товары в категории** через итератор (`CategoryIterator`).
- **Логировать создание объектов** через миксин `LogMixin`.
- **Работать с абстрактными классами** (`BaseProduct`, `BaseModel`).
- **Создавать заказы** (`Order`) с итоговой стоимостью.
- **Загружать данные из JSON** через `load_products_from_json`.
- **Проверять количество** — при создании товара с `quantity = 0` выбрасывается `ValueError`.
- **Считать среднюю цену** — в категории есть метод `middle_price()`, возвращающий среднюю цену товаров.
- **Обрабатывать исключения** — добавлено пользовательское исключение `ZeroQuantityError` 
с блоками `try/except/else/finally` (доп. задание).

---

## 🔒 Инкапсуляция: защита данных

Теперь важные данные в проекте защищены от случайного изменения:

- **Список товаров в категории** стал приватным (`__products`). Добавить товар можно только через метод `add_product`.
- **Цена товара** стала приватной (`__price`). Изменить её можно только через сеттер с проверкой:
  - если цена положительная — обновляется;
  - если цена <= 0 — выводится сообщение «Цена не должна быть нулевая или отрицательная», и цена остаётся прежней.

```python
from src.products import Product

product = Product("Ноутбук", "Игровой", 50000.0, 5)
product.price = 45000.0   # ✅ цена обновится
product.price = -1000.0   # ❌ выведет предупреждение, цена не изменится
print(product.price)      # 45000.0
```

---
## 🧩 Абстрактный класс и миксин
**BaseProduct** — абстрактный класс для всех продуктов
определяет обязательные свойства: `name, description, price, quantity`.
Все классы товаров наследуют его через `Product`.
Нельзя создать экземпляр `BaseProduct` напрямую — это контролируется абстракцией.

```python
from src.products import BaseProduct

# BaseProduct() — вызовет TypeError
```
#### LogMixin — логирование создания объектов
При создании любого объекта `Product` (или наследника) в консоль автоматически выводится `repr()` объекта.

```python
from src.products import Product

p = Product("Ноутбук", "Игровой", 1500.0, 3)
# Вывод в консоль: Product('Ноутбук', 'Игровой', 1500.0, 3)
```
Это помогает отслеживать, какие товары создаются и с какими параметрами.

---
# 🧬 Наследование и ограничения
Классы-наследники `Product`

**Smartphone** — добавляет атрибуты:

- efficiency — производительность (float)

- model — модель (str)

- memory — объём встроенной памяти в ГБ (int)

- color — цвет (str)

```python
from src.products import Smartphone

phone = Smartphone("Samsung Galaxy S23", "Флагман", 1000.0, 5, 95.5, "S23 Ultra", 256, "Черный")
```
**LawnGrass** — добавляет атрибуты:

- country — страна-производитель (str)

- germination_period — срок прорастания (str)

- color — цвет (str)

```python
from src.products import LawnGrass

grass = LawnGrass("Газонная трава", "Элитная трава", 500.0, 20, "Россия", "7 дней", "Зеленый")
```
#### Ограничения сложения (__add__)
Складывать (+) можно только товары одного класса. Проверка через type().

```python
from src.products import Smartphone, LawnGrass

phone1 = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")
phone2 = Smartphone("Apple", "", 1200, 3, 98.2, "15", 512, "Серебро")
print(phone1 + phone2)  # ✅ работает (8600.0)

grass = LawnGrass("Газон", "", 50, 100, "Россия", "14 дней", "Зелёный")
try:
    phone1 + grass  # ❌ TypeError
except TypeError as e:
    print(e)  # "Нельзя складывать Smartphone и LawnGrass"
```
#### Проверка добавления в категорию (add_product)
Метод add_product проверяет через `isinstance()`, что добавляется только объект `Product` или его наследник.

```python
from src.products import Category, Smartphone

category = Category("Смартфоны", "Описание", [])
phone = Smartphone("Samsung", "", 1000, 5, 95.5, "S23", 256, "Черный")

category.add_product(phone)  # ✅ работает
try:
    category.add_product("строка")  # ❌ TypeError
except TypeError as e:
    print(e)  # "В категорию можно добавлять только объекты Product или его наследников"
```
## 📦 Дополнительное задание: Заказ и абстрактный базовый класс
#### Класс Order
Хранит информацию о заказе на один товар:

- product — ссылка на товар

- quantity — количество

- total_price — итоговая стоимость (цена × количество)

```python
from src.products import Product, Order

product = Product("Ноутбук", "Игровой", 1500.0, 2)
order = Order(product, 3)
print(order)  # Заказ: Ноутбук, 3 шт., итого 4500.0 руб.
```
#### Абстрактный базовый класс BaseModel
Выделяет общие свойства name и description для классов `Category` и `Order`.
Оба класса наследуют `BaseModel`.

```python
from src.products import Category, Order, Product, BaseModel

category = Category("Электроника", "Описание", [])
product = Product("Ноутбук", "Игровой", 1500.0, 2)
order = Order(product, 3)

print(isinstance(category, BaseModel))  # True
print(isinstance(order, BaseModel))     # True
```

---
## ✨ Магические методы и итераторы
#### __str__ — строковое представление
```python
from src.products import Product, Category

product = Product("Смартфон", "AMOLED", 49999.0, 10)
category = Category("Электроника", "Гаджеты", [product])

print(product)   # Смартфон, 49999.0 руб. Остаток: 10 шт.
print(category)  # Электроника, количество продуктов: 10 шт.
```
#### __add__ — сложение товаров
```python
from src.products import Product

a = Product("А", "", 100, 10)
b = Product("Б", "", 200, 2)
print(a + b)  # 1400
```
#### Итератор для категорий
```python
from src.products import Product, Category

cat = Category("Электроника", "Гаджеты", [
    Product("Ноутбук", "", 1500.50, 3),
    Product("Мышь", "", 25.0, 50),
])

for product in cat:
    print(product)
```

---
## 📦 Удобное создание и загрузка
#### Класс-метод new_product
```python
from src.products import Product

data = {"name": "Наушники", "description": "Беспроводные", "price": 5000.0, "quantity": 20}
headphones = Product.new_product(data)
print(headphones)  # Наушники, 5000.0 руб. Остаток: 20 шт.
```
#### Проверка дубликатов
```python
from src.products import Product

existing = Product("Смартфон", "", 500.0, 10)
data = {"name": "Смартфон", "price": 600.0, "quantity": 5}
new_product = Product.new_product(data, [existing])
print(new_product.quantity)  # 15
print(new_product.price)     # 600.0
```
#### Загрузка из JSON
```python
from src.products import load_products_from_json

categories = load_products_from_json("data/products.json")
for cat in categories:
    print(f"Категория: {cat.name}")
    print(cat.products)
```

---
## 🧪 Тестирование и качество кода
```markdown
Проект покрыт тестами (92%), все **28 тестов** проходят.

```bash
# Запуск всех тестов с подробным выводом
poetry run pytest -v

# Проверка покрытия кода тестами (отчёт с пропущенными строками)
poetry run pytest --cov=src --cov-report=term-missing

# Проверка стиля кода (PEP8, максимальная длина строки 119)
poetry run flake8 src tests main.py --max-line-length=119

# Статическая проверка типов (mypy)
poetry run mypy src tests
```

---
## 🔧 Как запустить?
```bash
poetry run python main.py
```
Вывод в консоль покажет логи создания товаров через миксин, а затем все данные из `main.py`.

---
## 📦 Установка зависимостей
#### Проект использует Poetry:

```bash
poetry install --no-root
```
Основные зависимости: `pytest, pytest-cov, flake8, black, isort, mypy.`

---
## 📂 Структура проекта
```text
ecommerce_oop/
├── src/
│   └── products.py          # BaseProduct, LogMixin, Product, Smartphone, LawnGrass, Category, CategoryIterator, Order
├── tests/
│   └── test_products.py     # 28 теста
├── data/
│   └── products.json        # данные для загрузки (опционально)
├── main.py                  # точка входа
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md
```

## 🚨 Обработка исключений

### Проверка количества при создании товара
При создании объекта `Product` (или его наследников) с `quantity == 0` выбрасывается исключение `ValueError` с сообщением:
Товар с нулевым количеством не может быть добавлен

```text
Это же правило работает и при создании товара через класс-метод `new_product`.
```

```python
from src.products import Product

try:
    p = Product("Бракованный товар", "Описание", 100.0, 0)
except ValueError as e:
    print(e)  # Товар с нулевым количеством не может быть добавлен
```
Средняя цена в категории

В классе `Category` реализован метод `middle_price()`, который возвращает среднюю цену всех товаров в категории. 
Если категория пуста, метод возвращает `0.0`, чтобы избежать деления на ноль.

```python
from src.products import Product, Category

p1 = Product("Товар1", "", 100.0, 2)
p2 = Product("Товар2", "", 200.0, 3)
cat = Category("Категория", "Описание", [p1, p2])

print(cat.middle_price())  # 150.0

empty_cat = Category("Пустая", "Описание", [])
print(empty_cat.middle_price())  # 0.0
```
Пользовательское исключение (доп. задание)
Создан класс `ZeroQuantityError`. При попытке добавить товар с нулевым количеством в категорию `(через add_product)` 
или создать заказ `(Order)` с таким товаром выбрасывается это исключение. 
Обработка выполняется с блоками `try/except/else/finally:`

- except – выводит сообщение об ошибке;

- else – сообщает об успешном добавлении;

- finally – всегда выводит сообщение о завершении обработки.

```python
from src.products import Category, Product

cat = Category("Категория", "Описание", [])
p = Product("Тест", "", 100.0, 1)
p._quantity = 0  # имитируем нулевое количество

cat.add_product(p)
# В консоль выведется:
# Ошибка: Товар с нулевым количеством не может быть добавлен
# Обработка добавления товара завершена
```

---
## 👤 Об авторе
Меня зовут Александр `(GitHub: BUMbiro)`.

Я учусь Python-разработке, изучаю ООП, паттерны проектирования, тестирование и работу с типами.
Проект развивается от простых классов к абстракциям, миксинам и проверкам — с каждым заданием архитектура становится 
чище и надёжнее.

Спасибо, что заглянул в мой проект! 😎👍
