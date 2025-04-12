SCHEMAS = {
    "postgres": {
        "table": "postgres_users",
        "columns": {
            "id": "VARCHAR(100) PRIMARY KEY",
            "name": "VARCHAR(100)",
            "email": "VARCHAR(100)",
            "age": "INT"
        }
    },
    "mysql": {
        "table": "mysql_users",
        "columns": {
            "id": "VARCHAR(100) PRIMARY KEY",
            "name": "VARCHAR(100)",
            "email": "VARCHAR(100)",
            "age": "INT"
        }
    },
    "mongo": {
        "collection": "mongo_users",
        "fields": ["_id", "name", "email", "age"]
    }
}
