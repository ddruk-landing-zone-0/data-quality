CONSTRAINTS = {
    "postgres": {
        "test":{
                "count_rule": "SELECT COUNT(*) FROM postgres_users;",
                "rule0": "SELECT COUNT(*) FROM postgres_users WHERE email NOT LIKE '%.com';",
                "rule1": "SELECT COUNT(*) FROM postgres_users WHERE age < 20;"
        }
    },
    "mysql": {
            "test":{
                "count_rule": "SELECT COUNT(*) FROM mysql_users;",
                "rule0": "SELECT COUNT(*) FROM mysql_users WHERE email NOT LIKE '%.com';",
                "rule1": "SELECT COUNT(*) FROM mysql_users WHERE age < 20;"
        }
    },
    "mongo": {
        # For MongoDB, we'll use a custom object format
        "test":{
            "count_rule": {
                "operation": "count",
                "collection": "mongo_users"
            },
            "rule0": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "email": {"$not": {"$regex": "\\.com$"}}
                }
            },
            "rule1": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "age": {"$lt": 20}
                }
            }
        }
    }
}