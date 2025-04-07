import sqlite3
import random
from datetime import datetime, timedelta

# Инициализация БД
conn = sqlite3.connect('coffee.db')
cursor = conn.cursor()

# Создание таблиц
cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
)''')

cursor.execute('''
CREATE TABLE shops (
    shop_id INTEGER PRIMARY KEY,
    city TEXT,
    manager TEXT
)''')

cursor.execute('''
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    shop_id INTEGER,
    sale_date TEXT,
    quantity INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
)''')

# Заполнение данными
products = [
    (1, 'Эспрессо', 'Кофе', 2.5),
    (2, 'Латте', 'Кофе', 3.5),
    (3, 'Капучино', 'Кофе', 3.0),
    (4, 'Круассан', 'Еда', 2.0)
]
cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products)

shops = [
    (1, 'Москва', 'Иванов'),
    (2, 'Санкт-Петербург', 'Петрова')
]
cursor.executemany('INSERT INTO shops VALUES (?, ?, ?)', shops)

# Генерация 1000 случайных продаж
for i in range(1000):
    product_id = random.randint(1, 4)
    shop_id = random.randint(1, 2)
    sale_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    quantity = random.randint(1, 3)
    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', 
                  (i+1, product_id, shop_id, sale_date, quantity))

conn.commit()
conn.close()
