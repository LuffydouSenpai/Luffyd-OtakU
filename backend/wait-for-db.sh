#!/bin/sh

host="$1"
shift

echo "Waiting for PostgreSQL at $host..."

while ! nc -z "$host" 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"