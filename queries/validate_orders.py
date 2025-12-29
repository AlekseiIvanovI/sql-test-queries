import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')

queries = {
    "invoices_without_valid_customer": """
        SELECT InvoiceId, CustomerId 
        FROM Invoice 
        WHERE CustomerId NOT IN (SELECT CustomerId FROM Customer)
    """,
    "invoices_negative_total": """
        SELECT InvoiceId, Total 
        FROM Invoice 
        WHERE Total < 0
    """,
    "invoices_zero_items": """
        SELECT i.InvoiceId, i.InvoiceDate, i.Total
        FROM Invoice i
        LEFT JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
        GROUP BY i.InvoiceId
        HAVING COUNT(il.InvoiceLineId) = 0
    """,
    "high_value_invoices": """
        SELECT InvoiceId, CustomerId, Total 
        FROM Invoice 
        WHERE Total > 20 
        ORDER BY Total DESC 
        LIMIT 10
    """,
    "invoices_per_customer": """
        SELECT CustomerId, COUNT(*) AS invoice_count 
        FROM Invoice 
        GROUP BY CustomerId 
        ORDER BY invoice_count DESC 
        LIMIT 10
    """
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql.strip(), conn)
    records = len(df)
    suffix = "records" if "per_customer" in name or "high_value" in name else "issues"
    print(f"{name.upper()}: {records} {suffix}")
    df.to_csv(f"./reports/{name}.csv", index=False)

conn.close()