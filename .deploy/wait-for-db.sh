#!/bin/bash

# Wait for the PostgreSQL database to be ready
until PGPASSWORD=password psql -h "db" -U "user" -d "database" -c '\l'; do
  echo "Waiting for the database to be ready..."
  sleep 1
done

echo "Database is ready!"
