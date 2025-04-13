import requests
import os
from constraints import CONSTRAINTS
from typing import List, Any

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


def perform_checks(db_type, database):
    if db_type not in CONSTRAINTS:
        raise ValueError(f"Unsupported db type: {db_type}")
    if database not in CONSTRAINTS[db_type]:
        raise ValueError(f"Unsupported database: {database}")
    
    constraints = CONSTRAINTS[db_type][database]

    total_rows = 0
    results = []

    if "count_rule" not in constraints:
        raise ValueError(f"Count rule not found for database: {database}")
    try:
        count_result = requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json={
            "type": db_type,
            "database": database,
            "query": constraints["count_rule"]
        }).json()
        
        total_rows = count_result["result"][0][0] if db_type in ["postgres", "mysql"] else count_result["result"]["count"]
        print(f"Total rows in {database}: {total_rows}")
    except Exception as e:
        raise ValueError(f"Failed to execute count rule: {e}")
    

    for rule_id,constraint in constraints.items():
        if rule_id == "count_rule":
            continue
        
        query = constraint
        payload = {
            "type": db_type,
            "database": database,
            "query": query
        }

        print(f"Running query: {query}. URL: {GENERIC_CONNECTOR_URL}/execute")

        response = requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload)

        if response.status_code != 200:
            raise ValueError(f"Query execution failed: {response.text}")
        
        result = response.json()

        if "error" in result:
            print(f"Error in query result: {result['error']}")
            continue
        try:
            result = result["result"][0][0] if db_type in ["postgres", "mysql"] else result["result"]["count"]
            results.append({
                "rule_id": rule_id,
                "total_rows": total_rows,
                "total_rows_pass": result,
                "pass_percentage": (result / total_rows) * 100 if total_rows > 0 else 0,
            })
        except (KeyError, IndexError):
            # Handle unexpected result format
            print(f"Unexpected result format: {result}")

    return results

    
    
