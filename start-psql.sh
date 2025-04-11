#!/bin/bash

set -e

VERSION='14'
CLUSTER_NAME='main'

# Step 1: Update configs before starting
echo "listen_addresses = '*'" >> /etc/postgresql/$VERSION/$CLUSTER_NAME/postgresql.conf
echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/$VERSION/$CLUSTER_NAME/pg_hba.conf

# Step 2: Start cluster
pg_ctlcluster $VERSION $CLUSTER_NAME start

# Step 3: Wait until ready
until pg_isready -U postgres; do
  echo "⏳ Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Step 4: Create user
if [[ -n "$POSTGRES_USER" && -n "$POSTGRES_PASSWORD" ]]; then
  echo "Creating user: $POSTGRES_USER"

  if su - postgres -c "psql -c \"CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';\""; then
    echo "✅ User created."
  else
    echo "⚠️ User '${POSTGRES_USER}' might already exist."
  fi
else
  echo "POSTGRES_USER or POSTGRES_PASSWORD not set. Skipping user creation..."
fi

# Step 5: Create database
if [[ -n "$POSTGRES_DATABASE" ]]; then
  echo "Creating database: $POSTGRES_DATABASE"

  if su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DATABASE}'\" | grep -q 1"; then
    echo "⚠️ Database '${POSTGRES_DATABASE}' already exists."
  else
    su - postgres -c "psql -c \"CREATE DATABASE ${POSTGRES_DATABASE} OWNER ${POSTGRES_USER};\""
    echo "✅ Database '${POSTGRES_DATABASE}' created."
  fi
else
  echo "POSTGRES_DATABASE not set. Skipping database creation..."
fi

# Step 6: Restart with updated config
pg_ctlcluster $VERSION $CLUSTER_NAME restart
pg_lsclusters

# Step 7: Keep container alive
tail -f /dev/null
#!/bin/bash

set -e

VERSION='14'
CLUSTER_NAME='main'

# Step 1: Update configs before starting
echo "listen_addresses = '*'" >> /etc/postgresql/$VERSION/$CLUSTER_NAME/postgresql.conf
echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/$VERSION/$CLUSTER_NAME/pg_hba.conf

# Step 2: Start cluster
pg_ctlcluster $VERSION $CLUSTER_NAME start

# Step 3: Wait until ready
until pg_isready -U postgres; do
  echo "⏳ Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Step 4: Create user
if [[ -n "$POSTGRES_USER" && -n "$POSTGRES_PASSWORD" ]]; then
  echo "Creating user: $POSTGRES_USER"

  if su - postgres -c "psql -c \"CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';\""; then
    echo "✅ User created."
  else
    echo "⚠️ User '${POSTGRES_USER}' might already exist."
  fi
else
  echo "POSTGRES_USER or POSTGRES_PASSWORD not set. Skipping user creation..."
fi

# Step 5: Create database
if [[ -n "$POSTGRES_DATABASE" ]]; then
  echo "Creating database: $POSTGRES_DATABASE"

  if su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname='${POSTGRES_DATABASE}'\" | grep -q 1"; then
    echo "⚠️ Database '${POSTGRES_DATABASE}' already exists."
  else
    su - postgres -c "psql -c \"CREATE DATABASE ${POSTGRES_DATABASE} OWNER ${POSTGRES_USER};\""
    echo "✅ Database '${POSTGRES_DATABASE}' created."
  fi
else
  echo "POSTGRES_DATABASE not set. Skipping database creation..."
fi

# Step 6: Restart with updated config
pg_ctlcluster $VERSION $CLUSTER_NAME restart
pg_lsclusters

# Step 7: Keep container alive
tail -f /dev/null
