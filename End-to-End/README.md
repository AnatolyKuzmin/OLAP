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
1. Откройте ODBC Data Source Administrator (через поиск Windows).
2. Перейдите на вкладку System DSN → Add.
3. Выберите драйвер DuckDB и укажите параметры:
   - Data Source Name: CoffeeAnalytics
   - Database: Укажите полный путь к файлу coffee_olap.duckdb (например, C:\Users\Anatolii\CoffeeAnalytics\coffee_olap.duckdb)
4. Нажмите Test Connection → OK.

Подробная инструкция: [Настройка](https://github.com/AnatolyKuzmin/OLAP/blob/main/End-to-End/DSN_for_DuckDB.md) DSN (Data Source Name) для DuckDB в Windows

Шаг 3. Подключение Power BI к DuckDB
1. Откройте Power BI Desktop.
2. Get Data → ODBC → Connect. Выберите DSN CoffeeAnalytics
![image](https://github.com/user-attachments/assets/a7238490-1e4e-4d93-9227-e910b2333ec8)
![image](https://github.com/user-attachments/assets/9a7a597b-ad70-4101-bbab-a7326d9c93fa)
3. В окне Navigator выберите таблицы
4. Нажмите Load, чтобы загрузить данные.

Шаг 4. Создание отчета  
Пример 1: Анализ продаж по месяцам. На панели Visualizations выберите Line Chart. Настройте поля: Ось X: month (из sales_cube), Ось Y: total_revenue (сумма), Легенда: product (для разбивки по товарам)  
Пример 2: Карта магазинов. Выберите Map Visual. Настройте: Location: city (из shops), Size: total_revenue (из sales_cube)  
Пример 3: Топ-3 товара. Выберите Table Visual. Добавьте поля: product, total_revenue (сумма). Отсортируйте по убыванию выручки.  

Шаг 5. Публикация отчета (опционально)  
1. Нажмите Publish → выберите рабочую область в Power BI Service.  
2. Настройте автоматическое обновление (через Power BI Gateway, если нужно).
