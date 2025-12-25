import pandas as pd
import os

report = {
    "project": "SQL Test Data Validation",
    "database": "Chinook",
    "total_checks": 15,
    "issues_found": "See individual CSV reports",
    "recommendations": [
        "Fix duplicate emails",
        "Enforce NOT NULL on required customer fields",
        "Validate email format on insert",
        "Add check constraints for positive totals/quantities"
    ]
}

df = pd.DataFrame([{
    "Summary": "All critical validation checks completed",
    "Reports Generated": len([f for f in os.listdir('./reports') if f.endswith('.csv')])
}])

df.to_excel("./reports/SUMMARY_REPORT.xlsx", index=False)

print("Summary report generated: reports/SUMMARY_REPORT.xlsx")