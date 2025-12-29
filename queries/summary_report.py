import pandas as pd
import os

reports_dir = './reports'
csv_files = [f for f in os.listdir(reports_dir) if f.endswith('.csv')]

total_checks = len(csv_files)
total_issues = 0
issue_details = []

for csv_file in csv_files:
    path = os.path.join(reports_dir, csv_file)
    df = pd.read_csv(path)
    issues = len(df)
    total_issues += issues
    issue_details.append({"Check": csv_file.replace('.csv', ''), "Issues Found": issues})

summary_df = pd.DataFrame([
    {"Metric": "Project", "Value": "SQL Test Data Validation"},
    {"Metric": "Database", "Value": "Chinook"},
    {"Metric": "Total Checks Performed", "Value": total_checks},
    {"Metric": "Total Issues Found", "Value": total_issues},
    {"Metric": "Status", "Value": "Passed" if total_issues == 0 else "Issues Detected"}
])

details_df = pd.DataFrame(issue_details)

recommendations = pd.DataFrame({
    "Recommendations": [
        "Fix any duplicate emails if found",
        "Enforce NOT NULL on required customer fields",
        "Validate email format on data insert/update",
        "Add check constraints for positive totals/quantities/prices",
        "Ensure every invoice has at least one line item"
    ]
})

with pd.ExcelWriter('./reports/SUMMARY_REPORT.xlsx') as writer:
    summary_df.to_excel(writer, sheet_name='Overview', index=False)
    details_df.to_excel(writer, sheet_name='Issue Details', index=False)
    recommendations.to_excel(writer, sheet_name='Recommendations', index=False)

print("Summary report generated: reports/SUMMARY_REPORT.xlsx")