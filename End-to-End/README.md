# End-to-End OLAP для сети кофеен "CoffeeAnalytics"

**Технический стек для локального выполнения:**
- База данных: SQLite (для простоты)
- OLAP-движок: DuckDB (легковесный, но мощный)
- BI-визуализация: Metabase (OpenSource)
- Данные: Сгенерируем искусственные данные на Python

## Подготовка данных и схемы
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
