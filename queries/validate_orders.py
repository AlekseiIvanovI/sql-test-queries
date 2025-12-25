import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')

queries = {
    "orders_without_customer": "SELECT OrderId FROM Invoice WHERE CustomerId NOT IN (SELECT CustomerId FROM Customer)",
    "orders_negative_total": "SELECT InvoiceId, Total FROM Invoice WHERE Total < 0",
    "orders_zero_items": """
        SELECT i.InvoiceId 
        FROM Invoice i 
        LEFT JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId 
        GROUP BY i.InvoiceId 
        HAVING COUNT(il.InvoiceLineId) = 0
    """,
    "high_value_orders": "SELECT InvoiceId, Total FROM Invoice WHERE Total > 20 ORDER BY Total DESC LIMIT 10",
    "orders_per_customer": "SELECT CustomerId, COUNT(*) as order_count FROM Invoice GROUP BY CustomerId ORDER BY order_count DESC LIMIT 10"
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    df.to_csv(f"./reports/{name}.csv", index=False)
    print(f"{name.upper()}: {len(df)} records")

conn.close()