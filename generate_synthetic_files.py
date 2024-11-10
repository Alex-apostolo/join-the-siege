import pandas as pd
import random
from synthetic_file_generators.bank_statement_generator import generate_bank_statement
from synthetic_file_generators.invoice_generator import generate_invoice
from synthetic_file_generators.drivers_licence_generator import generate_drivers_license


# OCR error function with substitutions and deletions
def simulate_ocr_errors(text):
    text = text.translate(str.maketrans("OIBSGZ", "018562"))  # Substitute characters
    if random.choice([True, False]):  # Randomly delete 10% of characters
        text = "".join([c for c in text if random.random() > 0.1])
    return text


# Generate and apply OCR errors to records of each type
def generate_all_ocr_records():
    generators = [
        (generate_bank_statement, "bank_statement"),
        (generate_invoice, "invoice"),
        (generate_drivers_license, "driver_license"),
    ]
    ocr_records = []
    for generator, record_type in generators:
        for _ in range(200):
            record_str = generator()  # Generate string output
            ocr_record_str = simulate_ocr_errors(
                record_str
            )  # Apply OCR errors to the string
            ocr_records.append({"type": record_type, "text": ocr_record_str})
    return ocr_records


# Create and save the combined OCR dataset
pd.DataFrame(generate_all_ocr_records()).to_csv("combined_ocr.csv", index=False)
