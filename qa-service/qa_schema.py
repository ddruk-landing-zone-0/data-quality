QA_SCHEMA = {
    "postgres": {
        "table": "qa_logs",
        "columns": {
            "id": "SERIAL PRIMARY KEY",
            "test_time": "TIMESTAMP",
            "type": "TEXT",
            "db": "TEXT",
            "rule_type": "TEXT",
            "rule_id": "TEXT",
            "total_rows": "INT",
            "total_rows_pass": "INT",
            "pass_percentage": "FLOAT"
        }
    }
}