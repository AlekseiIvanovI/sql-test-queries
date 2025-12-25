# SQL Test Data Validation

**Senior QA Automation Engineer Portfolio Project**

**Aleksei Ivanov** · [aleksei.ivanov.qa@gmail.com](mailto:aleksei.ivanov.qa@gmail.com)

## Overview

Production-grade SQL validation queries using Python + sqlite3 + pandas on the Chinook database.

Demonstrates:
- Data integrity checks (duplicates, missing values, constraints)
- Business rule validation
- Automated reporting (CSV + Excel)

## Quick Start

```bash
pip install -r requirements.txt

python queries/validate_customers.py
python queries/validate_orders.py
python queries/validate_invoices.py
python queries/summary_report.py