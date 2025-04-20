from faker import Faker
import random
import uuid
from datetime import datetime

fake = Faker()

# Shared identity pool for consistent linking between user and employee
shared_identities = []

def get_shared_identity():
    """Retrieve or create a shared identity (name + email)."""
    if random.random() < 0.8 and shared_identities:
        return random.choice(shared_identities)
    identity = {
        "name": fake.name(),
        "email": fake.email()
    }
    shared_identities.append(identity)
    return identity

def generate_string_field(valid=True):
    return fake.word() if valid else ""

def generate_numeric_field():
    num = random.randint(1, 100)
    return -num if random.random() < 0.05 else num

def generate_sample(schema, table):
    sample = {}

    use_shared_identity = random.random() < 0.9 if "user" in table or "employee" in table else False
    identity = get_shared_identity() if use_shared_identity else {"name": fake.name(), "email": fake.email()}

    for field in schema:
        # UUIDs
        if field in ["id", "_id", "employee_id"]:
            sample[field] = str(uuid.uuid4())

        # Timestamp
        elif field == "timestamp":
            sample[field] = datetime.now().isoformat()

        # Email
        elif field == "email":
            sample[field] = identity["email"] if random.random() < 0.9 else fake.email()

        # Name fields
        elif field == "name":
            sample[field] = identity["name"]
        elif field == "employee_name":
            sample[field] = identity["name"] if random.random() < 0.8 else fake.name()

        # Age fields (numeric)
        elif field in ["age", "employee_age"]:
            sample[field] = generate_numeric_field()

        # Job-related field
        elif field == "department":
            sample[field] = generate_string_field(valid=random.random() < 0.8)

        # Default fallback for any other string field
        elif schema[field] in ["str", "string"]:
            sample[field] = generate_string_field(valid=random.random() < 0.8)

        # Default fallback for numeric type
        elif schema[field] in ["int", "float"]:
            sample[field] = generate_numeric_field()

        else:
            sample[field] = "N/A"

    return sample

def generate_samples(schema, table, n=10):
    return [generate_sample(schema, table) for _ in range(n)]

def generate_samples_for_all_tables(schema, n=10):
    all_samples = {}
    for table, fields in schema.items():
        if isinstance(fields, dict):
            all_samples[table] = generate_samples(fields, table, n)
        elif isinstance(fields, list):
            # Assuming list of field names
            all_samples[table] = generate_samples({field: "str" for field in fields}, table, n)
        else:
            raise ValueError(f"Invalid schema format for table {table}")
    return all_samples