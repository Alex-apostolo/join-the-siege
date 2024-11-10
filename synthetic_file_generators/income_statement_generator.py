import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Labels for income statement fields with optional selection
labels = {
    "header": ["INCOME STATEMENT", "PROFIT & LOSS", "EARNINGS REPORT"],
    "period": ["Reporting Period", "Period Ending", "Date"],
    "revenue": ["Revenue", "Total Sales", "Income"],
    "cogs": ["Cost of Goods Sold", "COGS"],
    "gross_profit": ["Gross Profit", "Gross Earnings"],
    "operating_expenses": ["Operating Expenses", "Expenses"],
    "operating_income": ["Operating Income", "Operating Profit"],
    "net_income": ["Net Income", "Net Profit", "Earnings"],
}

# Function to randomly select label or make it optional
def get_label(field):
    return f"{random.choice(labels[field])}: " if random.choice([True, False]) else ""

# Generate random income statement data
def generate_income_statement():
    # Define basic fields with calculations
    revenue = round(random.uniform(50000, 1000000), 2)
    cogs = round(revenue * random.uniform(0.3, 0.6), 2)  # Cost of goods sold as a percentage of revenue
    gross_profit = revenue - cogs
    operating_expenses = round(gross_profit * random.uniform(0.2, 0.5), 2)
    operating_income = gross_profit - operating_expenses
    net_income = operating_income - round(operating_income * random.uniform(0.1, 0.2), 2)  # Tax as a percentage of operating income

    # Random reporting period ending date
    period_end = (datetime.today() - timedelta(days=random.randint(0, 365))).date()

    # Structure the income statement with optional labels
    fields = {
        "header": random.choice(labels["header"]),
        "period": f"{get_label('period')}{period_end}",
        "revenue": f"{get_label('revenue')}${revenue:,.2f}",
        "cogs": f"{get_label('cogs')}${cogs:,.2f}",
        "gross_profit": f"{get_label('gross_profit')}${gross_profit:,.2f}",
        "operating_expenses": f"{get_label('operating_expenses')}${operating_expenses:,.2f}",
        "operating_income": f"{get_label('operating_income')}${operating_income:,.2f}",
        "net_income": f"{get_label('net_income')}${net_income:,.2f}",
    }

    # Join and return non-empty fields for final output
    return "\n".join(f"{data}" for data in fields.values() if data)
