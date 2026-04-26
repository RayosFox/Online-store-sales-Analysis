import sqlite3
import pandas as pd

conn = sqlite3.connect('ecommerce.db')

print("="*60)
print("1. ТОП-10 КЛИЕНТОВ ПО СУММЕ ПОКУПОК")
print("="*60)

query1 = """
WITH customer_spending AS (
    SELECT 
        o.customer_id,
        ROUND(SUM(oi.price), 2) as total_spent,
        COUNT(DISTINCT o.order_id) as orders_count
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY o.customer_id
)
SELECT 
    customer_id,
    total_spent,
    orders_count,
    ROUND(total_spent / orders_count, 2) as avg_order_value
FROM customer_spending
ORDER BY total_spent DESC
LIMIT 10
"""
df1 = pd.read_sql(query1, conn)
print(df1.to_string(index=False))

print("\n" + "="*60)
print("2. ОКОННАЯ ФУНКЦИЯ: СКОЛЬЗЯЩАЯ СРЕДНЯЯ ЗА 3 МЕСЯЦА")
print("="*60)

query2 = """
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', o.order_purchase_timestamp) as month,
        ROUND(SUM(oi.price), 2) as revenue,
        COUNT(DISTINCT o.order_id) as orders
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
)
SELECT 
    month,
    revenue,
    orders,
    ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) as rolling_avg_3m,
    ROUND(AVG(orders) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) as rolling_avg_orders
FROM monthly_revenue
ORDER BY month
"""
df2 = pd.read_sql(query2, conn)
print(df2.to_string(index=False))

print("\n" + "="*60)
print("3. ВОРОНКА ПРОДАЖ ПО СТАТУСАМ ЗАКАЗОВ")
print("="*60)

query3 = """
WITH funnel AS (
    SELECT 
        order_status,
        COUNT(*) as count
    FROM orders
    GROUP BY order_status
)
SELECT 
    order_status,
    count,
    ROUND(100.0 * count / (SELECT SUM(count) FROM funnel), 2) as percent
FROM funnel
ORDER BY count DESC
"""
df3 = pd.read_sql(query3, conn)
print(df3.to_string(index=False))

print("\n" + "="*60)
print("4. СЕЗОННОСТЬ ПРОДАЖ ПО МЕСЯЦАМ")
print("="*60)

query4 = """
SELECT 
    CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER) as month_num,
    CASE CAST(strftime('%m', o.order_purchase_timestamp) AS INTEGER)
        WHEN 1 THEN 'Янв'
        WHEN 2 THEN 'Фев'
        WHEN 3 THEN 'Мар'
        WHEN 4 THEN 'Апр'
        WHEN 5 THEN 'Май'
        WHEN 6 THEN 'Июн'
        WHEN 7 THEN 'Июл'
        WHEN 8 THEN 'Авг'
        WHEN 9 THEN 'Сен'
        WHEN 10 THEN 'Окт'
        WHEN 11 THEN 'Ноя'
        WHEN 12 THEN 'Дек'
    END as month_name,
    ROUND(SUM(oi.price), 2) as revenue,
    COUNT(DISTINCT o.order_id) as orders_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY month_num
ORDER BY revenue DESC
"""
df4 = pd.read_sql(query4, conn)
print(df4.to_string(index=False))

print("\n" + "="*60)
print("СОХРАНЕНИЕ ДАННЫХ ДЛЯ ДАШБОРДА")
print("="*60)

# Агрегированные данные для дашборда
query_dash = """
SELECT 
    strftime('%Y-%m', o.order_purchase_timestamp) as month,
    p.product_category_name,
    COUNT(DISTINCT o.order_id) as orders_count,
    ROUND(SUM(oi.price), 2) as revenue,
    ROUND(AVG(oi.price), 2) as avg_price,
    COUNT(oi.order_item_id) as items_sold
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY month, p.product_category_name
"""

df_dash = pd.read_sql(query_dash, conn)
df_dash.to_csv('dashboard_data.csv', index=False)
print(f"✓ Данные для дашборда сохранены: {len(df_dash)} строк")
print("✓ Файл 'dashboard_data.csv' создан")

# Теперь закрываем соединение
conn.close()

print("\n" + "="*60)
print("✅ ВСЕ ЗАПРОСЫ ВЫПОЛНЕНЫ УСПЕШНО!")
print("="*60)