import duckdb
import sqlite3

def sync_by_id():
    # Подключение к базам
    sqlite_conn = sqlite3.connect('coffee.db')
    duckdb_conn = duckdb.connect('coffee_olap.duckdb')
    
    # 1. Получаем максимальный ID в OLAP
    max_olap_id = duckdb_conn.sql('''
    SELECT COALESCE(MAX(sale_id), 0) 
    FROM sales
    ''').fetchone()[0]
    
    # 2. Загружаем недостающие данные из SQLite
    missing_data = sqlite_conn.execute(f'''
    SELECT * FROM sales 
    WHERE sale_id > {max_olap_id}
    ORDER BY sale_id
    ''').fetchall()
    
    # 3. Добавляем недостающие записи
    if missing_data:
        duckdb_conn.execute('BEGIN TRANSACTION')
        
        # Вставка порциями по 100 записей
        batch_size = 100
        for i in range(0, len(missing_data), batch_size):
            batch = missing_data[i:i + batch_size]
            duckdb_conn.executemany('''
            INSERT INTO sales VALUES (?, ?, ?, ?, ?)
            ''', batch)
        
        # 4. Проверяем расхождения (опционально)
        olap_count = duckdb_conn.sql('SELECT COUNT(*) FROM sales').fetchone()[0]
        sqlite_count = sqlite_conn.execute('SELECT COUNT(*) FROM sales').fetchone()[0]
        
        print(f'''
        Обновление завершено:
        - Добавлено записей: {len(missing_data)}
        - Всего в OLAP: {olap_count}
        - Всего в источнике: {sqlite_count}
        ''')
        
        duckdb_conn.execute('COMMIT')
    else:
        print("Данные уже синхронизированы")
    
    duckdb_conn.close()
    sqlite_conn.close()

if __name__ == '__main__':
    sync_by_id()
