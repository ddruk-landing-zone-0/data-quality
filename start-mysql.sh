#!/bin/bash

set -e

echo "[mysqld]\nbind-address = 0.0.0.0" > /etc/mysql/mysql.conf.d/my.cnf
echo "[mysqld]\nbind-address = 0.0.0.0" > /etc/mysql/mysql.conf.d/docker.cnf
echo "bind-address = 0.0.0.0" >> /etc/mysql/mysql.conf.d/mysql.cnf
echo "bind-address = 0.0.0.0" >> /etc/mysql/mysql.conf.d/mysqld.cnf

# Start MySQL server
sudo /etc/init.d/mysql start

# Wait for MySQL to be ready
sleep 5

if [[ -n "$MYSQL_USER" && -n "$MYSQL_PASSWORD" && -n "$MYSQL_DATABASE" ]]; then
  echo "Creating MySQL user and database..."

  sudo mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS \`$MYSQL_DATABASE\`;
CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
GRANT ALL PRIVILEGES ON \`$MYSQL_DATABASE\`.* TO '$MYSQL_USER'@'%';
FLUSH PRIVILEGES;
EOF

  echo "✅ MySQL user/database setup completed."
else
  echo "⚠️ MYSQL_USER, MYSQL_PASSWORD or MYSQL_DATABASE not set. Skipping creation."
fi

# Show databases
sudo mysql -u root -e "SHOW DATABASES;"

# Keep container running
tail -f /dev/null

