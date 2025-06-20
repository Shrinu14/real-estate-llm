#!/bin/bash

set -e

echo "📡 Waiting for services to become available..."

# Wait for MongoDB
until nc -z mongo-v2 27017; do
  echo "⏳ Waiting for MongoDB on port 27017..."
  sleep 2
done
echo "✅ MongoDB is up."

# Wait for Redis
until nc -z redis-v2 6379; do
  echo "⏳ Waiting for Redis on port 6379..."
  sleep 2
done
echo "✅ Redis is up."

# Wait for Milvus gRPC port
until nc -z milvus-standalone-v2 19530; do
  echo "⏳ Waiting for Milvus gRPC on port 19530..."
  sleep 2
done
echo "✅ Milvus gRPC is up."

# Wait for Milvus REST API (true readiness)
until curl -sf http://milvus-standalone-v2:19121 > /dev/null; do
  echo "⏳ Waiting for Milvus REST API on port 19121..."
  sleep 5
done
echo "✅ Milvus REST API is ready."

echo "🚀 All services ready. Starting the application..."

# Run the actual application command passed in CMD
exec "$@"
