import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in database:")
print(tables)

queries = {
    "duplicate_emails": "SELECT Email, COUNT(*) as count FROM Customer GROUP BY Email HAVING count > 1",
    "missing_required_fields": "SELECT CustomerId FROM Customer WHERE FirstName IS NULL OR LastName IS NULL OR Email IS NULL",
    "invalid_email_format": "SELECT CustomerId, Email FROM Customer WHERE Email NOT LIKE '%@%.%'",
    "customers_no_country": "SELECT CustomerId FROM Customer WHERE Country IS NULL OR Country = ''",
    "total_customers": "SELECT COUNT(*) as total FROM Customer"
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)
    if not df.empty:
        print(f"{name.upper()}: {len(df)} issues found")
        df.to_csv(f"./reports/{name}.csv", index=False)
    else:
        print(f"{name.upper()}: No issues")

conn.close()