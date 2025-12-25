import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')

queries = {
    "invoice_total_mismatch": """
        SELECT i.InvoiceId, i.Total as invoice_total, SUM(il.UnitPrice * il.Quantity) as calculated_total
        FROM Invoice i
        JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
        GROUP BY i.InvoiceId
        HAVING ABS(invoice_total - calculated_total) > 0.01
    """,
    "invoices_without_lines": """
        SELECT i.InvoiceId 
        FROM Invoice i 
        LEFT JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId 
        GROUP BY i.InvoiceId 
        HAVING COUNT(il.InvoiceLineId) = 0
    """,
    "negative_quantity": "SELECT InvoiceLineId FROM InvoiceLine WHERE Quantity <= 0",
    "zero_price_items": "SELECT InvoiceLineId FROM InvoiceLine WHERE UnitPrice <= 0",
    "invoice_date_future": "SELECT InvoiceId, InvoiceDate FROM Invoice WHERE InvoiceDate > date('now')"
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    df.to_csv(f"./reports/{name}.csv", index=False)
    print(f"{name.upper()}: {len(df)} issues")

conn.close()