# End-to-End OLAP для сети кофеен "CoffeeAnalytics"

**Технический стек для локального выполнения:**
- База данных: SQLite (для простоты)
- OLAP-движок: DuckDB (легковесный, но мощный)
- BI-визуализация: Metabase (OpenSource)
- Данные: Сгенерируем искусственные данные на Python

## Подготовка данных и схемы

Цель: Создать транзакционную базу данных с продажами кофе.

Шаг 1. Создадим транзакционную базу данных с продажами кофе.  
[generate_data.py](https://github.com/AnatolyKuzmin/OLAP/blob/main/End-to-End/generate_data.py)  

Шаг 2. Запуск генерации  
```
python generate_data.py
```
Файл `coffee.db` с таблицами:
- products (товары)
- shops (кофейни)
- sales (продажи)

Шаг 3. Проверка данных
Для проверки можно использовать DB Browser for SQLite.
![image](https://github.com/user-attachments/assets/ec685a90-b397-439a-b53a-e6cab626d11b)

## Создание OLAP-куба в DuckDB

Цель: Преобразовать транзакционные данные из SQLite в аналитический куб с помощью DuckDB.

Шаг 1. Установка DuckDB  
```
pip install duckdb
```

Шаг 2. Создание OLAP-структуры  
Создадим файл с помощью [build_olap.py](https://github.com/AnatolyKuzmin/OLAP/blob/main/End-to-End/build_olap.py)

Шаг 3. Запуск скрипта  
```
python build_olap.py
```
Файл `coffee_olap.duckdb` с:
- Таблицами-измерениями (products, shops).
- Факт-таблицей (sales).
- Представлением sales_cube (аналог OLAP-куба).

Шаг 4. Проверка куба  
Запустите интерактивный режим DuckDB через Windows(Python):
```
python -c "import duckdb; conn = duckdb.connect('coffee_olap.duckdb'); print(conn.sql('SELECT * FROM sales_cube LIMIT 5').fetchall())"
```
![image](https://github.com/user-attachments/assets/0c358d84-02da-4bb3-a0b5-1a5c05bda7d3)

## Автоматическое обновление OLAP-куба

Цель: Создать Python-скрипт для регулярного обновления данных с возможностью:
- Добавления новых продаж
- Обновления справочников
- Пересчета агрегаций

Шаг 1. Создаем скрипт обновления  
Скрипт для обновления [update_olap.py](https://github.com/AnatolyKuzmin/OLAP/blob/main/End-to-End/update_olap.py)

Шаг 2. Тестируем обновление  
Добавим новые данные в SQLite:
```
python -c "import sqlite3; conn = sqlite3.connect('coffee.db'); conn.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', [(1001, 2, 1, '2024-05-02', 1), (1002, 3, 2, '2024-05-03', 2)]); conn.commit(); conn.close()"
"
```
Запускаем скрипт для обнлваения OLAP
```
python update_olap.py
```
![image](https://github.com/user-attachments/assets/94cbbd4f-d955-41ad-b052-eb8070f26309)

Шаг 3. Проверяем результат
```
python -c "import duckdb; conn = duckdb.connect('coffee_olap.duckdb'); print(conn.sql('SELECT COUNT(*) FROM sales').fetchall())"
```

##  Настройка Excel для работы с OLAP-данными

Цель: Визуализировать данные из DuckDB через Power BI с созданием:
- Дашборда с KPI
- Интерактивных отчетов

Шаг 1. Установка драйвера DuckDB для Power BI  
Скачайте и установите ODBC-драйвер DuckDB для [Windows](https://duckdb.org/docs/stable/clients/odbc/windows)

Шаг 2. Настройка DSN (Data Source Name)

Шаг 3. Подключение Power BI к DuckDB

Шаг 4. Создание отчета
