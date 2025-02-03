#!/bin/bash


# Store the utilities
FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")
source "${ROOT}/setting/utils/tools.sh"

# Basic Parameters
NGINX_CONF="${ROOT}/setting/nginx.conf"
CONF="${ROOT}/setting/setting.json"
COMPOSE="${ROOT}/docker-compose.yml"
OPEN_WEB_UI_LOG_DIR="./open_web_ui"
OPEN_WEB_UI_LOG_FILE="openwebui.log"
# Check configuration is exit
check_config ${CONF}
check_jq

NGINX_PORT=$(cat "${CONF}" | jq -r '.nginx.port')
OPEN_WEB_UI_PORT=$(cat "${CONF}" | jq -r '.open_web_ui.port')
OLLAMA_PORT=$(cat "${CONF}" | jq -r '.ollama.port')
OLLAMA_MAX_LOADED_MODELS=$(cat "${CONF}" | jq -r '.ollama.OLLAMA_MAX_LOADED_MODELS')
MODEL_HANDLER_PORT=$(cat "${CONF}" | jq -r '.model_handler.port')

update_compose_env ${COMPOSE} "OLLAMA_MAX_LOADED_MODELS=${OLLAMA_MAX_LOADED_MODELS}"

update_docker_compose_port "$COMPOSE" "nginx" "$NGINX_PORT"
update_docker_compose_port "$COMPOSE" "open_webui" "$OPEN_WEB_UI_PORT"


#Use '-d' move service to background and than we can run the next code.
docker compose -f ${COMPOSE} up -d 

sleep 5

mkdir -p "$OPEN_WEB_UI_LOG_DIR"
docker logs -f open_webui 2>&1 | split -b 5M -d --filter='sh -c "cat > '${OPEN_WEB_UI_LOG_DIR}'/'${OPEN_WEB_UI_LOG_FILE}'"'
