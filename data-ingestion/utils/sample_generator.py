from faker import Faker
import random
import uuid

fake = Faker()

def generate_sample(schema):
    sample = {}
    for field in schema:
        if field in ["id", "_id"]:
            sample[field] = str(uuid.uuid4())
        elif field == "name":
            sample[field] = fake.name()
        elif field == "email":
            sample[field] = fake.email()
        elif field == "age":
            sample[field] = random.randint(18, 70)
        else:
            sample[field] = "N/A"
    return sample

def generate_samples(schema, n=10):
    return [generate_sample(schema) for _ in range(n)]
