import pandas as pd
import random
from synthetic_file_generators.bank_statement_generator import generate_bank_statement
from synthetic_file_generators.invoice_generator import generate_invoice
from synthetic_file_generators.drivers_licence_generator import generate_drivers_license
from synthetic_file_generators.balance_sheet_generator import generate_balance_sheet
from synthetic_file_generators.income_statement_generator import (
    generate_income_statement,
)


# OCR error function with deletions
def simulate_ocr_errors(text):
    text = "".join([c for c in text if random.random() > 0.1])
    return text


# Generate and apply OCR errors to records of each type
def generate_all_ocr_records():
    generators = [
        (generate_bank_statement, "bank_statement"),
        (generate_invoice, "invoice"),
        (generate_drivers_license, "driver_license"),
        (generate_income_statement, "income_statement"),
        (generate_balance_sheet, "balance_sheet"),
    ]

    return [
        {"type": record_type, "text": simulate_ocr_errors(generator())}
        for generator, record_type in generators
        for _ in range(100)
    ]


# Create and save the combined OCR dataset
pd.DataFrame(generate_all_ocr_records()).to_csv("combined_ocr.csv", index=False)
