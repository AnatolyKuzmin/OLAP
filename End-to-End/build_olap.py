import duckdb
import sqlite3

# Подключение к SQLite и DuckDB
sqlite_conn = sqlite3.connect('coffee.db')
duckdb_conn = duckdb.connect('coffee_olap.duckdb')

# Загрузка данных из SQLite в DuckDB
duckdb_conn.execute('''
CREATE TABLE products AS 
SELECT * FROM sqlite_scan('coffee.db', 'products')
''')

duckdb_conn.execute('''
CREATE TABLE shops AS 
SELECT * FROM sqlite_scan('coffee.db', 'shops')
''')

duckdb_conn.execute('''
CREATE TABLE sales AS 
SELECT * FROM sqlite_scan('coffee.db', 'sales')
''')

# Создание материализованного представления (аналог куба)
duckdb_conn.execute('''
CREATE VIEW sales_cube AS
SELECT 
    s.sale_date,
    EXTRACT(YEAR FROM CAST(s.sale_date AS DATE)) AS year,
    EXTRACT(MONTH FROM CAST(s.sale_date AS DATE)) AS month,
    p.category,
    p.name AS product,
    sh.city,
    sh.manager,
    SUM(s.quantity) AS total_quantity,
    SUM(s.quantity * p.price) AS total_revenue
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN shops sh ON s.shop_id = sh.shop_id
GROUP BY 
    s.sale_date, year, month, 
    p.category, p.name, sh.city, sh.manager
''')

# Проверка
result = duckdb_conn.sql('SELECT * FROM sales_cube LIMIT 5').fetchall()
print("Пример данных из куба:")
for row in result:
    print(row)

duckdb_conn.close()
sqlite_conn.close()
