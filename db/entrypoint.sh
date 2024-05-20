#!/bin/bash

echo "Changing password..."
echo "${RM_USER:-ryan}:${RM_PASSWORD:-123}" | chpasswd
echo "Starting SSH service..."
service ssh start
echo "Starting PostgreSQL..."
docker-entrypoint.sh postgres -c config_file=/etc/postgresql/postgresql.conf