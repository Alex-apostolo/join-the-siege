import random
from datetime import datetime
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Labels for balance sheet fields with optional selection
labels = {
    "header": ["BALANCE SHEET", "STATEMENT OF FINANCIAL POSITION"],
    "date": ["As of", "Date"],
    "assets": ["Total Assets", "Assets"],
    "liabilities": ["Total Liabilities", "Liabilities"],
    "equity": ["Shareholders' Equity", "Equity", "Net Worth"],
    "current_assets": ["Current Assets", "Short-term Assets"],
    "non_current_assets": ["Non-Current Assets", "Long-term Assets"],
    "current_liabilities": ["Current Liabilities", "Short-term Liabilities"],
    "non_current_liabilities": ["Non-Current Liabilities", "Long-term Liabilities"],
}

# Function to randomly select label or make it optional
def get_label(field):
    return f"{random.choice(labels[field])}: " if random.choice([True, False]) else ""

# Generate random balance sheet data
def generate_balance_sheet():
    # Set date for the balance sheet (e.g., end of a recent quarter or year)
    balance_date = datetime.today().date()
    
    # Assets and Liabilities calculations
    current_assets = round(random.uniform(50000, 500000), 2)
    non_current_assets = round(random.uniform(100000, 1000000), 2)
    total_assets = current_assets + non_current_assets

    current_liabilities = round(random.uniform(20000, 200000), 2)
    non_current_liabilities = round(random.uniform(50000, 300000), 2)
    total_liabilities = current_liabilities + non_current_liabilities

    equity = total_assets - total_liabilities  # Equity is the difference between assets and liabilities

    # Structure the balance sheet with optional labels
    fields = {
        "header": random.choice(labels["header"]),
        "date": f"{get_label('date')}{balance_date}",
        "assets": f"{get_label('assets')}${total_assets:,.2f}",
        "current_assets": f"{get_label('current_assets')}${current_assets:,.2f}",
        "non_current_assets": f"{get_label('non_current_assets')}${non_current_assets:,.2f}",
        "liabilities": f"{get_label('liabilities')}${total_liabilities:,.2f}",
        "current_liabilities": f"{get_label('current_liabilities')}${current_liabilities:,.2f}",
        "non_current_liabilities": f"{get_label('non_current_liabilities')}${non_current_liabilities:,.2f}",
        "equity": f"{get_label('equity')}${equity:,.2f}",
    }

    # Join and return non-empty fields for final output
    return "\n".join(f"{data}" for data in fields.values() if data)