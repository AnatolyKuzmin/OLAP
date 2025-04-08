import duckdb
import sqlite3
from datetime import datetime, timedelta

def update_olap():
    # Подключение к базам
    sqlite_conn = sqlite3.connect('coffee.db')
    duckdb_conn = duckdb.connect('coffee_olap.duckdb')
    
    # 1. Получаем дату последней продажи в OLAP
    last_date = duckdb_conn.sql('''
    SELECT MAX(CAST(sale_date AS DATE)) 
    FROM sales
    ''').fetchone()[0] or '2000-01-01'
    
    # 2. Загружаем новые данные из SQLite
    new_sales = sqlite_conn.execute(f'''
    SELECT * FROM sales 
    WHERE date(sale_date) > date('{last_date}')
    ''').fetchall()
    
    # 3. Добавляем новые данные в DuckDB
    if new_sales:
        duckdb_conn.execute('BEGIN TRANSACTION')
        duckdb_conn.executemany('''
        INSERT INTO sales VALUES (?, ?, ?, ?, ?)
        ''', new_sales)
        
        # 4. Обновляем справочники (полная перезагрузка)
        duckdb_conn.execute('DELETE FROM products')
        duckdb_conn.execute('''
        INSERT INTO products 
        SELECT * FROM sqlite_scan('coffee.db', 'products')
        ''')
        
        duckdb_conn.execute('COMMIT')
        print(f"Добавлено {len(new_sales)} новых записей")
    else:
        print("Нет новых данных для обновления")
    
    # 5. Обновляем представление куба (автоматически в DuckDB)
    duckdb_conn.close()
    sqlite_conn.close()

if __name__ == '__main__':
    update_olap()
