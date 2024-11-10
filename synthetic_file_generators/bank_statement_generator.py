from faker import Faker
import random

# Initialize Faker for generating realistic data
fake = Faker()

# Define possible labels for fields
labels = {
    "account_holder": ["Account Holder", "Account Name", "Holder Name"],
    "account_number": ["Account Number", "Acc No", "Account ID"],
    "bank_name": ["Bank Name", "Institution", "Financial Institution"],
    "statement_date": ["Statement Date", "Date", "Report Date"],
    "transaction_date": ["Transaction Date", "Date", "Txn Date"],
    "description": ["Description", "Transaction Details", "Txn Description"],
    "amount": ["Amount", "Txn Amount", "Debit/Credit"],
    "balance": ["Balance", "Available Balance", "Account Balance"]
}

# Function to randomly select label or make it optional
def get_label(field):
    return f"{random.choice(labels[field])}: " if random.choice([True, False]) else ""

# Function to create a simple text-based bank statement
def generate_bank_statement():
    # Bank account details
    account_holder = get_label("account_holder") + fake.name()
    account_number = get_label("account_number") + f"{random.randint(10000000, 99999999)}"
    bank_name = get_label("bank_name") + fake.company()
    
    # Statement details with optional labels
    statement_date = get_label("statement_date") + str(fake.date_this_year())
    
    # Generate a list of transactions
    transactions = []
    balance = round(random.uniform(5000, 10000), 2)  # Starting balance
    for _ in range(random.randint(5, 10)):
        transaction_date = get_label("transaction_date") + str(fake.date_between(start_date="-2y", end_date="today"))
        description = get_label("description") + fake.bs().capitalize()
        amount = round(random.uniform(-500, 500), 2)  # Random transaction amount
        balance += amount  # Update balance
        transactions.append(f"{transaction_date} | {description} | {get_label('amount')}${amount} | {get_label('balance')}${round(balance, 2)}")
    
    # Bank statement text
    bank_statement_text = f"""
    {account_holder}
    {account_number}
    {bank_name}

    {statement_date}

    Transactions:
    Date       | Description       | Amount       | Balance
    """ + "\n    ".join(transactions) + "\n"
    
    return bank_statement_text