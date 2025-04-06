# OLAP
Проектировать, наполнять и эффективно использовать OLAP-системы для аналитики и бизнес-отчетности.

## OLAP
Online Analytical Processing - это технология для быстрого анализа больших объемов данных. Главная задача OLAP – давать ответы на вопросы бизнеса быстро, даже если данных миллиарды строк.  
OLTP (Online Transaction Processing) — система обработки транзакций в реальном времени.  

Основное отличие OLTP от OLAP заключается в их назначении и использовании.  

OLTP (онлайн-обработка транзакций) предназначен для быстрого и эффективного управления повседневными транзакциями. Эти системы используют нормализованную структуру данных, оптимизируют операции записи и демонстрируют низкую задержку данных.  
OLAP (оперативная аналитическая обработка) используется для сложного анализа данных и принятия решений путём обработки больших объёмов исторических данных. Системы OLAP имеют денормализованную структуру данных, организуют данные в многомерные кубы, что сокращает время ответа на запросы и повышает производительность сложных запросов.  

Таким образом, OLTP ориентирован на обработку транзакций, а OLAP — на аналитическую обработку данных 25.

**Основные компоненты OLAP**  
- Куб(Cube) – многомерная структура данных. Пример: "Куб продаж" с измерениями: Время, Товар, Регион.
- Измерения (Dimensions) – "оси" анализа (например: время, география, продукт).
- Меры (Measures) – числовые значения для анализа (например: сумма продаж, количество).
- Иерархии (Hierarchies) – вложенные уровни (например: Год → Месяц → День).

**Типы OLAP**  
MOLAP (Multidimensional OLAP) – данные хранятся в специальном многомерном формате (высокая скорость, но долгая загрузка).  
ROLAP (Relational OLAP) – данные остаются в реляционной БД (гибкость, но медленнее).  
HOLAP (Hybrid OLAP) – комбинация MOLAP и ROLAP.

## Проектирование OLAP-кубов
**Схемы данных: "Звезда" vs "Снежинка"**  
![image](https://github.com/user-attachments/assets/108d239d-ae89-4991-8839-9a0ea7ebc2eb)
1. Звездообразная схема (Star Schema) – для большинства случаев (лучшая производительность).  
   Один центральный факт-таблица (например, Продажи) + несколько таблиц измерений (например, Товары, Магазины, Даты). Плюсы: Простота и высокая скорость запросов. Оптимальна для большинства OLAP-систем.
2. Снежинка (Snowflake Schema) – если важна экономия хранилища или есть сложные иерархии.  
   Таблицы измерений нормализованы (разбиты на подтаблицы). Например, Товары → Категории → Производители. Плюсы: Меньше избыточности данных. Минусы: Запросы сложнее и могут работать медленнее.  
**Факт-таблица (Fact Table)** Содержит числовые данные для анализа (меры): Сумма_продажи, Количество, Прибыль. Ссылается на измерения через внешние ключи: id_товара, id_магазина, id_даты.  
**Таблица измерений (Dimension Table)** Содержит описательные атрибуты: Товары: название, категория, бренд. Магазины: адрес, город, регион. Даты: день, месяц, год, квартал.

📌 Измерения должны быть полными (все возможные значения) и консистентными (одинаковые ключи во всех факт-таблицах).

Например:  
Цель: Спроектировать схему "звезда" для анализа продаж.  
- Факт-таблица (например, Сумма_продажи).
- Таблицы измерений (например, Товары, Магазины, Даты).
- Иерархии (например, Категория → Товар).
```
Факт-таблица "Продажи":
- id_товара (FK)
- id_магазина (FK)
- id_даты (FK)
- Сумма_продажи
- Количество

Измерения:
1. "Товары":
   - id_товара (PK)
   - Название
   - Категория
   - Производитель

2. "Магазины":
   - id_магазина (PK)
   - Город
   - Регион
   - Страна

3. "Даты":
   - id_даты (PK)
   - День
   - Месяц
   - Квартал
   - Год
```
Чтобы OLAP работал быстро, важно: *Партиционирование* – разбить факт-таблицу по периодам (например, по годам). *Агрегаты* – предварительный расчет сумм по месяцам/кварталам. *Индексы* – ускоряют поиск по измерениям.

## Наполнение OLAP (ETL и загрузка данных)
ETL (Extract, Transform, Load) — процесс:  
- **Extract (Извлечение)** – получение данных из источников.
  Источники данных: Реляционные БД (MySQL, PostgreSQL, SQL Server). Файлы (CSV, Excel, JSON). API (Google Analytics, CRM-системы).  
  📌 Определить, какие данные нужны для измерений и фактов. Учесть инкрементальную загрузку (догрузка только новых данных).  
- **Transform (Трансформация)** – очистка, преобразование, агрегация.  
  ✅ Очистка данных: Заполнение пропусков (например, Unknown для пустых городов). Исправление форматов (даты → YYYY-MM-DD). Удаление дубликатов.  
  ✅ Преобразование данных: Расчет новых полей (например, Прибыль = Цена - Себестоимость). Агрегация (суммы продаж по дням/месяцам).  
  ✅ Согласование измерений (Slowly Changing Dimensions, SCD): Как обновлять изменяющиеся данные (например, если клиент сменил адрес)? Типы SCD: SCD Type 1 – перезапись (старые данные теряются). SCD Type 2 – сохранение истории (новая запись + дата актуальности).  
- **Load (Загрузка)** – размещение данных в OLAP-хранилище.
  Факт-таблицы: обычно загружаются полностью (но можно и инкрементально). Измерения: обновляются по мере изменений (SCD).

Инструменты для ETL. SQL (INSERT/UPDATE) - Ручные скрипты - Для простых случаев. SSIS (Microsoft) - Встроен в SQL Server - Для корпоративных решений на MS-стеке. Talend - Open-source ETL - Гибкость, поддержка многих источников. Apache Airflow - Оркестрация ETL-пайплайнов	- Для сложных процессов с расписанием. dbt (Data Build Tool) - Трансформация в SQL - Современный подход, работает с облачными DWH.

Например:  
Цель: Создать простой ETL-процесс для загрузки данных в OLAP.  
1. Данные: Возьмём [CSV-файл](https://github.com/AnatolyKuzmin/OLAP/blob/main/sales-data.csv) с продажами.  
2. Extract: Загрузим данные в промежуточную таблицу (например, в PostgreSQL или Python/pandas).  
3. Transform: Очистим данные (пропуски, дубли). Добавим расчетные поля (Прибыль = Revenue - Cost). Приведим даты к единому формату.  
4. Load: Загрузим данные в структуру "звезда" (факт-таблица + измерения).

📌 Пример [кода](https://github.com/AnatolyKuzmin/OLAP/blob/main/sales-data.py) (Python + pandas):
```
import pandas as pd

# Extract
df = pd.read_csv("sales-data.csv")

# Transform
df['Profit'] = df['Revenue'] - df['Cost']
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Load (в условную БД)
df.to_sql('sales_fact', con=database_engine, if_exists='replace')
```
🚀 Инкрементальная загрузка – обновлять только новые данные (например, по дате).  
🚀 Параллельная обработка – разбивать данные на потоки.  
🚀 Кэширование промежуточных результатов.  

## Языки запросов и аналитика
**MDX (Multidimensional Expressions)** — это специализированный язык запросов, разработанный для работы с многомерными базами данных, такими как OLAP-кубы. Он похож на SQL, но оптимизирован для анализа данных в нескольких измерениях.  
📌 Пример простого MDX-запроса  
```
SELECT 
  {[Measures].[Sales Amount], [Measures].[Profit]} ON COLUMNS,
  {[Product].[Category].Members} ON ROWS
FROM 
  [Sales Cube]
WHERE 
  ([Time].[2023], [Geography].[Europe])``
```

**DAX (Data Analysis Expressions)** — это язык формул и выражений, разработанный Microsoft для анализа данных и создания вычислений в таких инструментах, как: Power BI, Power Pivot (в Excel), SQL Server Analysis Services (SSAS) Tabular.  
📌 Примеры DAX  
```
\\ Простая мера (общая сумма продаж)
Total Sales = SUM(Sales[Amount])
\\ Мера с условием (продажи только красных товаров)
Red Sales = CALCULATE(SUM(Sales[Amount]), Products[Color] = "Red")
\\ Вычисляемый столбец (прибыль = доход - затраты)
Profit = Sales[Revenue] - Sales[Cost]
```

**SQL для ROLAP**  
📌 Пример SQL  
```
SELECT 
    d1.attribute1, 
    d2.attribute2,
    SUM(f.sales) AS total_sales,
    AVG(f.quantity) AS avg_quantity,
    COUNT(*) AS transaction_count
FROM 
    fact_table f
JOIN 
    dimension1 d1 ON f.dim1_key = d1.key
JOIN 
    dimension2 d2 ON f.dim2_key = d2.key
GROUP BY 
    d1.attribute1, d2.attribute2
```

Визуализация результатов  
- **Power BI**: Лучше всего работает с DAX. Поддержка DirectQuery к OLAP-кубам.  
- **Excel**: Связь с кубами через Power Pivot. Создание сводных таблиц.  
- **Tableau**: Подключение через JDBC/ODBC. Использование MDX для кастомных мер.  

## Оптимизация и администрирование
Стратегии партиционирования  
- По дате: Разделение факт-таблиц по годам/кварталам  
- По бизнес-сущностям: Например, отдельные партиции по регионам  
- Hot/Cold данные: Активные данные на SSD, архив на HDD

**Пример (SQL Server)**
```
-- Создание партиционированной таблицы
CREATE PARTITION FUNCTION pf_ByYear (int)
AS RANGE RIGHT FOR VALUES (2020, 2021, 2022, 2023)

CREATE PARTITION SCHEME ps_ByYear
AS PARTITION pf_ByYear
TO (fg_2020, fg_2021, fg_2022, fg_2023, fg_Current)
```
Выбор типа хранения  
Columnstore - Факт-таблицы, аналитика - SQL Server Columnstore  
Rowstore - Таблицы измерений - Классические B-деревья  
Aggregations - Предрасчитанные итоги - SSAS Aggregations  

Materialized Views (Pre-aggregations). Технологии: SSAS: Aggregations, Oracle: Materialized Views, ClickHouse: AggregatingMergeTree
Пример:  
```
-- Oracle Materialized View
CREATE MATERIALIZED VIEW mv_sales_monthly
REFRESH COMPLETE ON DEMAND
AS 
SELECT 
  TRUNC(sale_date, 'MONTH') AS month,
  product_id,
  SUM(amount) AS total_amount
FROM sales
GROUP BY TRUNC(sale_date, 'MONTH'), product_id;
```
Паттерны для ускорения: Избегайте CROSSJOIN с большими измерениями. Используйте NON EMPTY в MDX. В DAX применяйте CALCULATE с фильтрами вместо вложенных FILTER.

Плохой MDX:  
```
SELECT {[Measures].[Sales]} ON 0,
CrossJoin([Product].[Category].Members, [Date].[Year].Members) ON 1
FROM [Cube]
```
Оптимизированный MDX:
```
SELECT {[Measures].[Sales]} ON 0,
NON EMPTY [Product].[Category].Members * [Date].[Year].Members ON 1
FROM [Cube]
```

## Безопасность в OLAP
**RLS (Row-Level Security)** - это функция безопасности в системах управления базами данных, которая позволяет ограничивать доступ к строкам таблицы на основе характеристик пользователя, выполняющего запрос.   
**Ролевая модель (RBAC)** – это модель управления доступом, в которой права на выполнение операций назначаются ролям, а пользователи получают эти права через назначенные им роли.  
**Логирование**. Ключевые события для логирования Попытки доступа к запрещенным измерениям, Изменения схемы кубов, Массовый экспорт данных.  

## Интеграция с BI-инструментами

## Современные OLAP-решения

## Проект
