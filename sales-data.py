import pandas as pd

# Extract
df = pd.read_csv("sales-data.csv")

# Transform
df['Profit'] = df['Revenue'] - df['Cost']
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

# Load (в условную БД)
df.to_sql('sales_fact', con=database_engine, if_exists='replace')
