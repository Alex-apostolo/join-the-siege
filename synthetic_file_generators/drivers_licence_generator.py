import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# Predefined license formats and classes
license_formats = [
    lambda: f"D{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
    lambda: f"{random.randint(1000, 9999)}-{random.randint(100, 999)}-{random.choice('ABCDEFGH')}{random.randint(10, 99)}",
    lambda: f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(10000, 99999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}",
]

license_classes = [
    "A",
    "B",
    "C",
    "D",
    "M",
    "A1",
    "A2",
    "B1",
    "C1",
    "D1",
    "LMV",
    "MCWG",
    "HGV",
    "PVG",
    "Class 1",
    "Class 2",
    "Class 3",
    "Class 4",
]

# Labels for driver's license fields
labels = {
    "header": ["DRIVER LICENSE", "DRIVING LICENCE", "LICENSE", "IDENTIFICATION"],
    "license_number": ["License Number", "DL No.", "ID No."],
    "name": ["Full Name", "Name", "Driver Name"],
    "dob": ["Date of Birth", "DOB", "Birth Date"],
    "issue_date": ["Issue Date", "Issued On", "Date of Issue"],
    "exp_date": ["Expiration Date", "Expires On", "Expiry Date"],
    "license_class": ["Class", "License Class", "Category"],
    "address": ["Address", "Residence", "Home Address"],
    "gender": ["Gender", "Sex"],
    "country": ["Country", "Nation", "Issued In"],
    "jurisdiction": ["Jurisdiction", "Region", "State"],
}


# Function to randomly select label or make it optional
def get_label(field):
    return f"{random.choice(labels[field])}: " if random.choice([True, False]) else ""


# Generate a formatted driver's license with optional labels
def generate_drivers_license():
    country = fake.country()
    address = fake.address().replace("\n", ", ")

    fields = {
        "header": random.choice(labels["header"]),
        "license_number": f"{get_label('license_number')}{random.choice(license_formats)()}",
        "name": f"{get_label('name')}{fake.first_name()} {fake.last_name()}",
        "dob": f"{get_label('dob')}{fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()}",
        "issue_date": f"{get_label('issue_date')}{(datetime.today() - timedelta(days=random.randint(0, 3650))).date()}",
        "exp_date": f"{get_label('exp_date')}{(datetime.today() + timedelta(days=random.randint(1825, 3650))).date()}",
        "license_class": f"{get_label('license_class')}{random.choice(license_classes)}",
        "address": f"{get_label('address')}{address}",
        "gender": f"{get_label('gender')}{random.choice(['Male', 'Female', 'Non-Binary'])}",
        "country": f"{get_label('country')}{country}",
        "jurisdiction": f"{get_label('jurisdiction')}{fake.state_abbr() if country == 'United States' else country}",
    }

    # Join and return non-empty fields for final output
    return "\n".join(f"{data}" for data in fields.values() if data)
