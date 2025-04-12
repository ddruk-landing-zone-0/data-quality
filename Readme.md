# Multicontainer System For Data Quality

## Current state

1. Service: Postgres

Data persistence issue. Data lost after container restart.

2. Service: Mysql

- Data persistence critical issue. Data lost after each new connection establishment.
- Container crash sometimes


3. Service: Mongo

Data persistence issue. Data lost after container restart.

4. Service: connector-server

Ok

5. Service: data-ingestion-server

Ok

6. Service: qa-service

Pending

7. Service: qa-postgress

Pending