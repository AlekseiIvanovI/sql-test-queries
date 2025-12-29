import sqlite3
import pandas as pd

conn = sqlite3.connect('chinook.db')

# List tables for verification
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in database:")
print(tables)

queries = {
    "duplicate_emails": "SELECT Email, COUNT(*) as count FROM Customer GROUP BY Email HAVING count > 1",
    "missing_required_fields": "SELECT CustomerId, FirstName, LastName, Email FROM Customer WHERE FirstName IS NULL OR LastName IS NULL OR Email IS NULL",
    "invalid_email_format": "SELECT CustomerId, Email FROM Customer WHERE Email NOT LIKE '%@%.%' OR Email NOT LIKE '%.__%'",
    "customers_no_country": "SELECT CustomerId, Country FROM Customer WHERE Country IS NULL OR TRIM(Country) = ''",
    # Informational only - not an "issue"
    "total_customers": "SELECT COUNT(*) AS total_customers FROM Customer"
}

for name, sql in queries.items():
    df = pd.read_sql_query(sql, conn)

    if name == "total_customers":
        count = df.iloc[0]['total_customers'] if not df.empty else 0
        print(f"TOTAL_CUSTOMERS: {count} customers in database")
        df.to_csv(f"./reports/{name}.csv", index=False)
    elif not df.empty:
        print(f"{name.upper()}: {len(df)} issues found")
        df.to_csv(f"./reports/{name}.csv", index=False)
    else:
        print(f"{name.upper()}: No issues")

conn.close()