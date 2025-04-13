SCHEMAS = {
    "postgres": {
        "test":{
            "table": "postgres_users",
            "columns": {
                "id": "VARCHAR(100) PRIMARY KEY",
                "name": "VARCHAR(100)",
                "email": "VARCHAR(100)",
                "age": "INT"
            }
        }
    },
    "mysql": {
        "test": {
            "table": "mysql_users",
            "columns": {
                "id": "VARCHAR(100) PRIMARY KEY",
                "name": "VARCHAR(100)",
                "email": "VARCHAR(100)",
                "age": "INT"
            }
        }
    },
    "mongo": {
        "test": {
            "collection": "mongo_users",
            "fields": ["_id", "name", "email", "age"]
        }
    }
}
