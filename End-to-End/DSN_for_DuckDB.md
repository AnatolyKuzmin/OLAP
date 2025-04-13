## Настройка DSN (Data Source Name) для DuckDB в Windows

### 1. Открытие ODBC Data Source Administrator
- Нажмите Win + R, введите odbcad32.exe и нажмите Enter.
- Перейдите на вкладку System DSN (не User DSN!)
### 2. Добавление нового источника данных
- Нажмите кнопку Add (Добавить).
- В списке драйверов выберите DuckDB Driver.  
Если драйвера нет в списке: Скачайте последнюю версию с официального сайта DuckDB. Установите .msi-файл от администратора
### 3. Конфигурация DSN
- Data Source Name	CoffeeAnalytics (любое понятное имя)
- Database	Укажите полный путь к файлу .duckdb
![image](https://github.com/user-attachments/assets/69acb2f9-24bc-44a1-8aab-257351325d9f)
### 4. Дополнительные настройки (опционально)
- Read Only: Для запрета изменений данных из Power BI
- Time Zone: UTC (если работаете с разными часовыми поясами)
### 5. Проверка подключения
- Нажмите кнопку Test Connection.
- Если всё настроено правильно, увидите сообщение: Connection successful to database: [ваш_путь]
- Нажмите OK для сохранения DSN.
### 6. Проблемы и решения
- Ошибка "Data source name not found":
  - Проверьте, что создали DSN во вкладке System, а не User
  - Перезапустите Power BI
- Ошибка доступа к файлу:
  - Убедитесь, что файл .duckdb существует по указанному пути
  - Проверьте права доступа: кликните правой кнопкой на файле → Свойства → Безопасность
- Драйвер не отображается: powershell
```
# Проверить установленные драйверы ODBC
Get-OdbcDriver -Name "*duckdb*"
```
### 7. Альтернативный метод (без DSN)
Если не хотите создавать DSN, можно подключиться напрямую через строку соединения в Power BI:
- Выберите Get Data → ODBC → Advanced options
- В поле Connection string введите:
```
Driver=DuckDB Driver;Database=C:\path\to\coffee_olap.duckdb
```
