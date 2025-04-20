SCHEMAS = {
    "postgres": {
        "test":{
            "postgres_users": {
                "id": "VARCHAR(100) PRIMARY KEY",
                "timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "name": "VARCHAR(100)",
                "email": "VARCHAR(100)",
                "age": "INT"
            },
            "postgres_employee_details":{
                "id": "VARCHAR(100) PRIMARY KEY",
                "email": "VARCHAR(100)",
                "employee_id": "VARCHAR(100)",
                "employee_name": "VARCHAR(100)",
                "employee_age": "INT",
                "department": "VARCHAR(100)"
            }
        }
    },
    "mysql": {
        "test": {
            "mysql_users": {
                "id": "VARCHAR(100) PRIMARY KEY",
                "timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                "name": "VARCHAR(100)",
                "email": "VARCHAR(100)",
                "age": "INT"
            },
            "mysql_employee_details": {
                "id": "VARCHAR(100) PRIMARY KEY",
                "email": "VARCHAR(100)",
                "employee_id": "VARCHAR(100)",
                "employee_name": "VARCHAR(100)",
                "employee_age": "INT",
                "department": "VARCHAR(100)"
            }
        }
    },
    "mongo": {
        "test": 
            {
                "mongo_users":["_id", "timestamp", "name", "email", "age"],
                "mongo_employee_details": ["_id", "email", "employee_id", "employee_name", "employee_age", "department"]
            }
    }
}
