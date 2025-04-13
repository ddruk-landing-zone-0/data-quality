# Multicontainer System for Data Quality

## Current System Status

### 1. **Postgres**
- Data persistence issue: Data is lost after container restart.

### 2. **MySQL**
- Critical data persistence issue: Data is lost after each new connection.
- Occasional container crashes.

### 3. **MongoDB**
- Data persistence issue: Data is lost after container restart.

### 4. **Connector Server**
- ✅ Functioning correctly.

### 5. **Data Ingestion Server**
- ✅ Functioning correctly.

### 6. **QA Service**
- ✅ Functioning correctly.

### 7. **QA Postgres**
- ✅ Functioning correctly.

---

## How To run

```
docker compose up --build -d
docker ps
docker compose logs
docker compose down
```

---


## Available Endpoints

### 1. **Connection Endpoint** `[POST]`
`http://127.0.0.1:5001/connect`

#### Request Body:
```json
{
  "type": "postgres",
  "username": "admin",
  "password": "admin",
  "database": "test",
  "host": "my-postgres-container-0",
  "port": "5432"
}
```

#### Expected Response:
```json
{
  "message": "postgres connected successfully."
}
```

---

### 2. **Execute Query Endpoint** `[POST]`
`http://127.0.0.1:5001/execute`

#### Request Body:
```json
{
  "type": "mysql",
  "query": "SELECT * FROM mysql_users"
}
```

#### Expected Response:
```json
{
  "result": [
    
  ]
}
```

---

### 3. **Ingest Endpoint** `[POST]`
`http://127.0.0.1:5050/ingest`

#### Request Body:
```json
{
  "type": "postgres",
  "database": "test"
}
```

---

### 4. **QA Check Endpoint** `[POST]`
`http://127.0.0.1:9090/perform-check`

#### Request Body:
```json
{
  "type": "postgres",
  "database": "test"
}
```

#### Expected Response:
```json
{
  "check_response": [
    {
      "pass_percentage": 66.875,
      "rule_id": "rule0",
      "total_rows": 160,
      "total_rows_pass": 107
    },
    {
      "pass_percentage": 5.625,
      "rule_id": "rule1",
      "total_rows": 160,
      "total_rows_pass": 9
    }
  ],
  "connect_response": {
    "message": "postgres connected successfully."
  },
  "create_table_response": {
    "result": []
  },
  "qa_db_response": {
    "message": "postgres connected successfully."
  },
  "store_response": {
    "result": []
  }
}
```

---

### 5. **QA Result Query** `[POST]`
`http://127.0.0.1:5001/execute`

#### Request Body:
```json
{
  "type": "postgres",
  "database": "qa_db",
  "query": "SELECT * FROM qa_logs;"
}
```

#### Expected Response:
```json
{
  "result": [
    [
      1,
      "Sun, 13 Apr 2025 16:28:17 GMT",
      "postgres",
      "qa_db",
      "rule0",
      230,
      159,
      69.1304347826087
    ],
    [
      2,
      "Sun, 13 Apr 2025 16:28:17 GMT",
      "postgres",
      "qa_db",
      "rule1",
      230,
      2,
      0.8695652173913043
    ]
  ]
}
```
