import os
import requests

GENERIC_CONNECTOR_URL = os.getenv("GENERIC_CONNECTOR_URL", "http://connector-server:5000")

def connect_to_db(db_type):
    creds = {
        "postgres": {
            "host": os.getenv("POSTGRES_HOST", "my-postgres-container-0"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
            "username": os.getenv("POSTGRES_USER", "admin"),
            "password": os.getenv("POSTGRES_PASSWORD", "admin"),
            "database": os.getenv("POSTGRES_DATABASE", "test"),
        },
        "mysql": {
            "host": os.getenv("MYSQL_HOST", "my-mysql-container-0"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "username": os.getenv("MYSQL_USER", "admin"),
            "password": os.getenv("MYSQL_PASSWORD", "admin"),
            "database": os.getenv("MYSQL_DATABASE", "test"),
        },
        "mongo": {
            "host": os.getenv("MONGO_HOST", "my-mongo-container-0"),
            "port": os.getenv("MONGO_PORT", "27017"),
            "username": os.getenv("MONGO_USER", "admin"),
            "password": os.getenv("MONGO_PASSWORD", "admin"),
            "database": os.getenv("MONGO_DATABASE", "test"),
        }
    }

    payload = {"type": db_type, ** creds[db_type]}
    print(f"Connecting to {db_type} with payload: {payload}. URL: {GENERIC_CONNECTOR_URL}/connect")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/connect", json=payload).json()

def insert_to_db(db_type, samples):
    if db_type in ["postgres", "mysql"]:
        values = ", ".join(
            f"('{s['id']}', '{s['name']}', '{s['email']}', {s['age']})" for s in samples
        )
        query = f"INSERT INTO users (id, name, email, age) VALUES {values};"
        payload = {"type": db_type, "query": query}
    elif db_type == "mongo":
        payload = {
            "type": db_type,
            "query": {
                "operation": "insert",
                "collection": "users",
                "documents": samples
            }
        }
    else:
        raise ValueError("Unsupported DB type")

    return requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload).json()
