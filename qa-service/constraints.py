CONSTRAINTS = {
    "postgres": {
        "test":{
                "count_rule": "SELECT COUNT(*) FROM postgres_users;",
                "accuracy":{
                    "timestamp_validity": "SELECT COUNT(*) FROM postgres_users WHERE timestamp > '2000-01-01' AND timestamp < '2025-12-31';",
                    "age_validity": "SELECT COUNT(*) FROM postgres_users WHERE age > 0 AND age < 120;",
                    "email_validity": "SELECT COUNT(*) FROM postgres_users WHERE email LIKE '%@%.%';",
                    "employee_age_validity": "SELECT COUNT(*) FROM postgres_employee_details WHERE employee_age > 0 AND employee_age < 120;"
                },
                "completeness":{
                    "id_completeness": "SELECT COUNT(*) FROM postgres_users WHERE id IS NOT NULL AND id != '';",
                    "email_completeness": "SELECT COUNT(*) FROM postgres_users WHERE email IS NOT NULL AND email != '';",
                    "name_completeness": "SELECT COUNT(*) FROM postgres_users WHERE name IS NOT NULL AND name != '';",
                    "employee_id_completeness": "SELECT COUNT(*) FROM postgres_employee_details WHERE employee_id IS NOT NULL AND employee_id != '';",
                    "employee_name_completeness": "SELECT COUNT(*) FROM postgres_employee_details WHERE employee_name IS NOT NULL AND employee_name != '';"
                },
                "consistency":{
                    "email_consistency": "SELECT COUNT(*) FROM postgres_users WHERE email IN (SELECT email FROM postgres_employee_details);",
                    "employee_name_consistency": "SELECT COUNT(*) FROM postgres_employee_details WHERE employee_name IN (SELECT name FROM postgres_users);"
                },
                "validity":{
                    "email_validity": "SELECT COUNT(*) FROM postgres_users WHERE email NOT LIKE '%@%.%';",
                    "age_validity": "SELECT COUNT(*) FROM postgres_users WHERE age < 0 OR age > 120;",
                    "employee_age_validity": "SELECT COUNT(*) FROM postgres_employee_details WHERE employee_age < 0 OR employee_age > 120;"
                },
                "timeliness":{
                }
    }
    },
    "mysql": {
            "test":{
                "count_rule": "SELECT COUNT(*) FROM mysql_users;",
                "accuracy":{
                    "timestamp_validity": "SELECT COUNT(*) FROM mysql_users WHERE timestamp > '2000-01-01' AND timestamp < '2025-12-31';",
                    "age_validity": "SELECT COUNT(*) FROM mysql_users WHERE age > 0 AND age < 120;",
                    "email_validity": "SELECT COUNT(*) FROM mysql_users WHERE email LIKE '%@%.%';",
                    "employee_age_validity": "SELECT COUNT(*) FROM mysql_employee_details WHERE employee_age > 0 AND employee_age < 120;"
                },
                "completeness":{
                    "id_completeness": "SELECT COUNT(*) FROM mysql_users WHERE id IS NOT NULL AND id != '';",
                    "email_completeness": "SELECT COUNT(*) FROM mysql_users WHERE email IS NOT NULL AND email != '';",
                    "name_completeness": "SELECT COUNT(*) FROM mysql_users WHERE name IS NOT NULL AND name != '';",
                    "employee_id_completeness": "SELECT COUNT(*) FROM mysql_employee_details WHERE employee_id IS NOT NULL AND employee_id != '';",
                    "employee_name_completeness": "SELECT COUNT(*) FROM mysql_employee_details WHERE employee_name IS NOT NULL AND employee_name != '';"
                },
                "consistency":{
                    "email_consistency": "SELECT COUNT(*) FROM mysql_users WHERE email IN (SELECT email FROM mysql_employee_details);",
                    "employee_name_consistency": "SELECT COUNT(*) FROM mysql_employee_details WHERE employee_name IN (SELECT name FROM mysql_users);"
                },
                "validity":{
                    "email_validity": "SELECT COUNT(*) FROM mysql_users WHERE email NOT LIKE '%@%.%';",
                    "age_validity": "SELECT COUNT(*) FROM mysql_users WHERE age < 0 OR age > 120;",
                    "employee_age_validity": "SELECT COUNT(*) FROM mysql_employee_details WHERE employee_age < 0 OR employee_age > 120;"
                },
                "timeliness":{
                }
        }
    },
"mongo": {
    "test": {
        "count_rule": {
            "operation": "count",
            "collection": "mongo_users"
        },
        "accuracy": {
            "timestamp_validity": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "timestamp": {
                        "$gt": { "$date": "2000-01-01T00:00:00Z" },
                        "$lt": { "$date": "2025-12-31T00:00:00Z" }
                    }
                }
            },
            "age_validity": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "age": { "$gt": 0, "$lt": 120 }
                }
            },
            "email_validity": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "email": { "$regex": "@.*\\..*", "$options": "i" }
                }
            },
            "employee_age_validity": {
                "operation": "count",
                "collection": "mongo_employee_details",
                "filter": {
                    "employee_age": { "$gt": 0, "$lt": 120 }
                }
            }
        },
        "completeness": {
            "id_completeness": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "_id": { "$exists": True }
                }
            },
            "email_completeness": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "email": { "$exists": True, "$ne": "" }
                }
            },
            "name_completeness": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "name": { "$exists": True, "$ne": "" }
                }
            },
            "employee_id_completeness": {
                "operation": "count",
                "collection": "mongo_employee_details",
                "filter": {
                    "employee_id": { "$exists": True, "$ne": "" }
                }
            },
            "employee_name_completeness": {
                "operation": "count",
                "collection": "mongo_employee_details",
                "filter": {
                    "employee_name": { "$exists": True, "$ne": "" }
                }
            }
        },
        "consistency": {
        },
        "validity": {
            "email_validity": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "email": { "$not": { "$regex": "@.*\\..*", "$options": "i" } }
                }
            },
            "age_validity": {
                "operation": "count",
                "collection": "mongo_users",
                "filter": {
                    "$or": [
                        { "age": { "$lt": 0 } },
                        { "age": { "$gt": 120 } }
                    ]
                }
            },
            "employee_age_validity": {
                "operation": "count",
                "collection": "mongo_employee_details",
                "filter": {
                    "$or": [
                        { "employee_age": { "$lt": 0 } },
                        { "employee_age": { "$gt": 120 } }
                    ]
                }
            }
        },
        "timeliness": {
            # MongoDB-specific logic for timeliness can be added here
        }
    }
}
}