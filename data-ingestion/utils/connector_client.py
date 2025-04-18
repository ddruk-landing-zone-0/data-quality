import os
import requests
from schemas import SCHEMAS

GENERIC_CONNECTOR_URL = os.getenv("GENERIC_CONNECTOR_URL", "http://connector-server:5000")

def connect_to_db(db_type,database):
     
    creds = {
        f"postgres_{database}": {
            "host": os.getenv("POSTGRES_HOST", "my-postgres-container-0"),
            "port": os.getenv("POSTGRES_PORT", "5432"),
            "username": os.getenv("POSTGRES_USER", "admin"),
            "password": os.getenv("POSTGRES_PASSWORD", "admin"),
            "database": os.getenv("POSTGRES_DATABASE", "test"),
        },
        f"mysql_{database}": {
            "host": os.getenv("MYSQL_HOST", "my-mysql-container-0"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "username": os.getenv("MYSQL_USER", "admin"),
            "password": os.getenv("MYSQL_PASSWORD", "admin"),
            "database": os.getenv("MYSQL_DATABASE", "test"),
        },
        f"mongo_{database}": {
            "host": os.getenv("MONGO_HOST", "my-mongo-container-0"),
            "port": os.getenv("MONGO_PORT", "27017"),
            "username": os.getenv("MONGO_USER", "admin"),
            "password": os.getenv("MONGO_PASSWORD", "admin"),
            "database": os.getenv("MONGO_DATABASE", "test"),
        }
    }

    payload = {"type": db_type, **creds[f"{db_type}_{database}"]}
    print(f"Connecting to {db_type} with payload: {payload}. URL: {GENERIC_CONNECTOR_URL}/connect")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/connect", json=payload).json()

def create_table_if_not_exists(db_type, database):
    schema = SCHEMAS[db_type][database]

    if db_type in ["postgres", "mysql"]:
        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in schema["columns"].items()])
        query = f"CREATE TABLE IF NOT EXISTS {schema['table']} ({columns_def});"
        payload = {
            "type": db_type,
            "database": database,
            "query": query
        }

    elif db_type == "mongo":
        # MongoDB creates collection on insert, but we can ensure index/collection creation
        payload = {
            "type": db_type,
            "database": database,
            "query": {
                "operation": "insert",
                "collection": schema["collection"],
                "documents": []  # No-op insert to trigger collection creation
            }
        }

    else:
        raise ValueError(f"Unsupported DB type: {db_type}")

    print(f"Ensuring schema for {db_type} with: {payload}")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload).json()

def insert_to_db(db_type, database, samples):
    schema = SCHEMAS[db_type][database]
    table = schema.get("table", "users")

    if db_type in ["postgres", "mysql"]:
        values = ", ".join(
            f"('{s['id']}', '{s['name']}', '{s['email']}', {s['age']})" for s in samples
        )
        query = f"INSERT INTO {table} (id, name, email, age) VALUES {values};"
        payload = {"type": db_type, "database": database,"query": query}

    elif db_type == "mongo":
        payload = {
            "type": db_type,
            "database": database,
            "query": {
                "operation": "insert",
                "collection": schema["collection"],
                "documents": samples
            }
        }

    else:
        raise ValueError("Unsupported DB type")
    

    print(f"Inserting data into {db_type} with: {payload}")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload).json()
