#!/bin/bash

set -e

sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf


# Start MongoDB
/usr/bin/mongod --fork --logpath /var/log/mongodb.log --dbpath /var/lib/mongodb --bind_ip_all

# Wait for Mongo to initialize
sleep 3

if [[ -n "$MONGO_USER" && -n "$MONGO_PASSWORD" && -n "$MONGO_DATABASE" ]]; then
  echo "Creating MongoDB user and database..."

  /usr/bin/mongosh --quiet <<EOF
use $MONGO_DATABASE
db.createUser({
  user: "$MONGO_USER",
  pwd: "$MONGO_PASSWORD",
  roles: [ { role: "readWrite", db: "$MONGO_DATABASE" } ]
})
EOF

  echo "✅ MongoDB user/database created."
else
  echo "⚠️ MONGO_USER, MONGO_PASSWORD or MONGO_DATABASE not set. Skipping creation."
fi

# Show databases
/usr/bin/mongosh --eval "db.adminCommand('listDatabases')"

# Keep container running
tail -f /dev/null

