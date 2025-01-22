#!/bin/bash


# Store the utilities
FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")
source "${ROOT}/setting/utils/tools.sh"

# Basic Parameters
NGINX_CONF="${ROOT}/setting/nginx.conf"
CONF="${ROOT}/setting/setting.json"
COMPOSE="${ROOT}/docker-compose.yml"

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


docker compose -f ${COMPOSE} up