#!/bin/bash

set -e  # 出錯即退出
# WAITING_TIME=8
FILE=$(realpath "$0")
ROOT=$(dirname "$FILE")
cd "$ROOT/.."  # CD to root path

CONF="${ROOT}/setting/setting.json"
COMPOSE_FILE="${ROOT}/docker-compose.yml"
TOOLS="${ROOT}/setting/utils/tools.sh"

# Get tools
source "$TOOLS"
check_config "$CONF"
check_jq

# Get chatbot launch port.
CHATBOT_PORT=$(jq -r '.chatbot.port' "$CONF")


# Run Docker Compose
docker compose -f "$COMPOSE_FILE" up -d --force-recreate
# while [ $WAITING_TIME -gt 0 ]; do
#     echo -ne "Waiting to start Accelbrain... $WAITING_TIME s\r"
#     sleep 1
#     ((WAITING_TIME--))
# done
echo "✅ Lunching！AccelBrain：http://127.0.0.1:${CHATBOT_PORT}"
# xdg-open http://127.0.0.1:${CHATBOT_PORT}
