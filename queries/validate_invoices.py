import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')

queries = {
    "invoice_total_mismatch": """
        SELECT 
            i.InvoiceId, 
            i.Total AS invoice_total, 
            ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS calculated_total,
            ABS(i.Total - ROUND(SUM(il.UnitPrice * il.Quantity), 2)) AS difference
        FROM Invoice i
        JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
        GROUP BY i.InvoiceId
        HAVING difference > 0.01
    """,
    "invoices_without_lines": """
        SELECT i.InvoiceId, i.InvoiceDate, i.Total
        FROM Invoice i
        LEFT JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
        GROUP BY i.InvoiceId
        HAVING COUNT(il.InvoiceLineId) = 0
    """,
    "negative_quantity": """
        SELECT InvoiceLineId, InvoiceId, Quantity 
        FROM InvoiceLine 
        WHERE Quantity <= 0
    """,
    "zero_price_items": """
        SELECT InvoiceLineId, InvoiceId, UnitPrice 
        FROM InvoiceLine 
        WHERE UnitPrice <= 0
    """,
    "invoice_date_future": """
        SELECT InvoiceId, InvoiceDate 
        FROM Invoice 
        WHERE InvoiceDate > date('now')
    """
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql.strip(), conn)
    issues = len(df)
    print(f"{name.upper()}: {issues} issues")
    df.to_csv(f"./reports/{name}.csv", index=False)

conn.close()