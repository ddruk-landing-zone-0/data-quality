import requests
import os
from datetime import datetime
import json
from qa_schema import QA_SCHEMA

GENERIC_CONNECTOR_URL = os.getenv("GENERIC_CONNECTOR_URL", "http://connector-server:5000")


def connect_to_qa_db(qa_db_creds):
    payload = {"type": "postgres", **qa_db_creds}
    print(f"Connecting to postgres with payload: {payload}. URL: {GENERIC_CONNECTOR_URL}/connect")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/connect", json=payload).json()


def create_qa_table_if_not_exists(db_type , database , table):
    schema = QA_SCHEMA

    if db_type == "postgres":
        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in schema[db_type]["columns"].items()])
        query = f"CREATE TABLE IF NOT EXISTS {schema['postgres']['table']} ({columns_def});"
        payload = {
            "type": db_type,
            "database": database,
            "query": query
        }
    else:
        raise ValueError(f"Unsupported db type: {db_type}")

    print(f"Creating table if not exists with payload: {payload}. URL: {GENERIC_CONNECTOR_URL}/execute")
    return requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload).json()



def store_log_check_result(target_db_type, target_database, db_type,database,table,results):
    entries = []

    for result in results:
        entry = {
            "test_time": datetime.now().isoformat(),
            "type": target_db_type,
            "db": target_database,
            "rule_id": result["rule_id"],
            "total_rows": result["total_rows"],
            "total_rows_pass": result["total_rows_pass"],
            "pass_percentage": result["pass_percentage"]
        }
        entries.append(entry)
    
    values = ", ".join([f"('{entry['test_time']}', '{entry['type']}', '{entry['db']}', '{entry['rule_id']}', {entry['total_rows']}, {entry['total_rows_pass']}, {entry['pass_percentage']})" for entry in entries])
    query = f"INSERT INTO {table} (test_time, type, db, rule_id, total_rows, total_rows_pass, pass_percentage) VALUES {values};"

    payload = {
        "type": db_type,
        "database": database,
        "query": query
    }

    # Assuming the table name is qa_db_log
    print(f"Storing log check result with payload: {payload}. URL: {GENERIC_CONNECTOR_URL}/execute")

    response = requests.post(f"{GENERIC_CONNECTOR_URL}/execute", json=payload)

    if response.status_code != 200:
        raise ValueError(f"Failed to store log check result: {response.text}")
    return response.json()
