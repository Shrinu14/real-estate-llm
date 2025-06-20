#!/bin/bash

set -e

echo "📡 Waiting for services to become available..."

# Wait for MongoDB (default port 27017)
until nc -z mongo 27017; do
  echo "⏳ Waiting for MongoDB on port 27017..."
  sleep 2
done
echo "✅ MongoDB is up."

# Wait for Redis (default port 6379)
until nc -z redis 6379; do
  echo "⏳ Waiting for Redis on port 6379..."
  sleep 2
done
echo "✅ Redis is up."

# Wait for Milvus (gRPC port 19530)
until nc -z milvusdbb 19530; do
  echo "⏳ Waiting for Milvus gRPC on port 19530..."
  sleep 2
done
echo "✅ Milvus is up."

# Optionally wait longer for Milvus internal readiness (retrying connection can help)
echo "⏳ Giving Milvus a few extra seconds to finish internal setup..."
sleep 10

echo "🚀 All services ready. Starting the application..."

# Run the application (passed as CMD in Dockerfile)
exec "$@"
