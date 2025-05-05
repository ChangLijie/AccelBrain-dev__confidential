#!/bin/bash

# Store the utilities
FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")

# Basic Parameters
COMPOSE="${ROOT}/docker-compose.yml"
echo "🛑 Stop Docker Compose service..."
docker compose -f "${COMPOSE}" down
echo "✅ AccelBrain is closed。"
