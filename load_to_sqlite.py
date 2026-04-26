import pandas as pd
import sqlite3
import os

# Создаем соединение с базой данных
conn = sqlite3.connect('ecommerce.db')

# Список файлов для загрузки (укажи свои имена)
files = {
    'olist_orders_dataset.csv': 'orders',
    'olist_order_items_dataset.csv': 'order_items',
    'olist_products_dataset.csv': 'products',
    'olist_customers_dataset.csv': 'customers'
}

for file, table in files.items():
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.to_sql(table, conn, if_exists='replace', index=False)
        print(f"✓ Загружена таблица {table}: {len(df)} строк")
    else:
        print(f"✗ Файл {file} не найден")

print("\nГотово! База данных 'ecommerce.db' создана")
conn.close()