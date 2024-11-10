from faker import Faker
import random
from datetime import timedelta

# Initialize Faker for generating random data
fake = Faker()

# Define possible labels for fields
labels = {
    "company_name": ["Company Name", "Business Name", "Firm"],
    "customer_company": ["Customer Company", "Client Company", "Customer Firm"],
    "contact_name": ["Contact Name", "Customer Contact", "Client"],
    "address": ["Address", "Location", "Customer Address"],
    "phone": ["Phone", "Contact Number", "Phone Number"],
    "email": ["Email", "Contact Email", "Email Address"],
    "website": ["Website", "URL", "Company Site"],
    "invoice_number": ["Invoice Number", "Invoice ID", "Bill No"],
    "issue_date": ["Issue Date", "Date of Issue", "Billing Date"],
    "due_date": ["Due Date", "Payment Due", "Expiry Date"],
    "subtotal": ["Subtotal", "Amount Before Tax", "Pre-Tax Total"],
    "tax": ["Tax", "Tax Amount", "Additional Tax"],
    "total": ["Total", "Total Due", "Grand Total"],
    "bank_details": ["Bank No", "Bank Account", "Bank"],
    "payment_email": ["Payment Email", "Contact for Payment", "Billing Email"],
}


# Function to randomly select label or make it optional
def get_label(field):
    return f"{random.choice(labels[field])}: " if random.choice([True, False]) else ""


# Function to create a simple text-based invoice
def generate_invoice():
    # Automatically generate an invoice ID
    invoice_id = f"INV-{random.randint(1000, 9999)}"

    # Basic invoice details with optional labels
    company_name = get_label("company_name") + fake.company()
    customer_name = get_label("contact_name") + fake.name()
    customer_company = get_label("customer_company") + fake.company()
    address = get_label("address") + fake.address()
    phone = get_label("phone") + fake.phone_number()
    email = get_label("email") + fake.email()
    website = get_label("website") + fake.url()

    invoice_date = get_label("issue_date") + str(fake.date_this_year())
    due_date = get_label("due_date") + str(
        fake.date_this_year() + timedelta(days=random.randint(15, 45))
    )

    # Invoice line items with optional labels
    line_items = []
    total_amount = 0
    for _ in range(random.randint(2, 5)):
        description = fake.bs().capitalize()
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(10, 100), 2)
        line_total = round(quantity * unit_price, 2)
        total_amount += line_total
        line_items.append(f"{description}: {quantity} x ${unit_price} = ${line_total}")

    # Tax and total calculation
    tax_rate = 0.05  # 5% tax
    tax_amount = round(total_amount * tax_rate, 2)
    total_with_tax = total_amount + tax_amount

    # Invoice text with optional labels
    invoice_text = (
        f"""
    {company_name}
    {customer_company}
    {customer_name}
    {address}
    {phone}
    {email}
    {website}

    {get_label("invoice_number")}{invoice_id}
    {invoice_date}
    {due_date}

    Items:
    """
        + "\n    ".join(line_items)
        + f"""

    {get_label("subtotal")}${total_amount}
    {get_label("tax")}${tax_amount}
    {get_label("total")}${total_with_tax}

    Payment Instructions:
    {get_label("bank_details")}123-456-7890 | Bank Name: Studio Shodwe
    {get_label("payment_email")}hello@reallygreatsite.com
    """
    )
    return invoice_text
