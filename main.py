from src.products import Product, Category

if __name__ == "__main__":
    # Создаём товары
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14
    )
    product4 = Product(
        '55" QLED 4K',
        "Фоновая подсветка",
        123000.0,
        7
    )

    # Создаём категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4]
    )

    # ---- Демонстрация __str__ ----
    print("=" * 50)
    print("Товары (__str__):")
    print(product1)
    print(product2)
    print(product3)
    print(product4)
    print()

    # ---- Демонстрация __str__ для категорий ----
    print("=" * 50)
    print("Категории (__str__):")
    print(category1)
    print(category2)
    print()

    # ---- Демонстрация геттера products (вывод списка товаров) ----
    print("=" * 50)
    print("Список товаров в категории 'Смартфоны':")
    print(category1.products)
    print()

    # ---- Демонстрация __add__ (сложение товаров) ----
    print("=" * 50)
    print("Сложение товаров (общая стоимость на складе):")
    print(f"{product1.name} + {product2.name} = {product1 + product2} руб.")
    print(f"{product1.name} + {product3.name} = {product1 + product3} руб.")
    print(f"{product2.name} + {product3.name} = {product2 + product3} руб.")
    print()

    # ---- Демонстрация итератора (for product in category) ----
    print("=" * 50)
    print("Перебор товаров в категории 'Смартфоны' (итератор):")
    for product in category1:
        print(f"  - {product}")
    print()

    # ---- Статистика ----
    print("=" * 50)
    print("Статистика:")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров (уникальных): {Category.product_count}")
