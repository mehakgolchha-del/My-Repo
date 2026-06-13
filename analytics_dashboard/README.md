"""Analytics Dashboard Documentation."""

# Analytics Dashboard Module

Track finances, generate business reports, and visualize data with interactive charts.

## Features

- **Transaction Tracking**: Record income and expenses
- **Budget Management**: Set and monitor budgets
- **Financial Reports**: Generate comprehensive financial reports
- **Category Analysis**: Breakdown expenses by category
- **Metrics Tracking**: Track business KPIs
- **Data Visualization**: Create interactive charts with Plotly
- **Monthly Summaries**: Analyze monthly trends

## Quick Start

```python
from analytics_dashboard.analytics import Analytics

analytics = Analytics()

# Add transactions
analytics.add_transaction(
    date="2024-01-15",
    category="Salary",
    amount=5000,
    transaction_type="income"
)

analytics.add_transaction(
    date="2024-01-20",
    category="Groceries",
    amount=200,
    transaction_type="expense"
)

# Get balance
balance = analytics.get_balance()
print(f"Net Balance: ${balance['net_balance']}")

# Get monthly summary
monthly = analytics.get_monthly_summary("2024-01")
print(f"Monthly Income: ${monthly['income']}")

# Generate report
report = analytics.generate_report("2024-01-01", "2024-01-31")
print(report)

# Create visualization
analytics.create_expense_chart()
```

## API Reference

### Analytics

- `add_transaction(date, category, amount, type, description)`: Record a transaction
- `get_balance()`: Get total income, expense, and net balance
- `get_monthly_summary(month)`: Get monthly summary
- `get_category_breakdown()`: Get expenses by category
- `create_expense_chart(output_path)`: Generate expense pie chart
- `generate_report(start_date, end_date)`: Generate financial report
- `track_metric(metric_name, value, date)`: Track business metrics

## Transaction Types

- `income`: Money coming in
- `expense`: Money going out

## Date Format

All dates should be in `YYYY-MM-DD` format.

## Database

Data is stored in SQLite database at `./data/analytics.db` (configurable in config.yaml).

Tables:
- `transactions`: Income and expense records
- `budgets`: Budget limits by category
- `metrics`: Business metrics over time

## Example Report Output

```json
{
    "period": "2024-01-01 to 2024-01-31",
    "total_income": 5000,
    "total_expense": 450,
    "net_balance": 4550,
    "transaction_count": 5,
    "average_transaction": 890
}
```

## Visualization

Expense charts are saved as interactive HTML files that can be opened in any web browser.

## Notes

- All amounts should be in your preferred currency unit
- Charts require Plotly to be installed
- Database operations are automatic and handled internally
