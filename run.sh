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



update_nginx_listen_port "$NGINX_CONF" "$NGINX_PORT"
if [ $? -ne 0 ]; then
    echo "Failed to update the Nginx configuration."
    exit 1
fi


update_compose_env ${COMPOSE} "OLLAMA_MAX_LOADED_MODELS=${OLLAMA_MAX_LOADED_MODELS}"

update_docker_compose_port "$COMPOSE" "nginx" "$NGINX_PORT"
update_docker_compose_port "$COMPOSE" "model_handler" "$MODEL_HANDLER_PORT"
update_docker_compose_port "$COMPOSE" "ollama" "$OLLAMA_PORT"
update_docker_compose_port "$COMPOSE" "open_webui" "$OPEN_WEB_UI_PORT"

# echo ${NGINX_PORT}
# echo ${MODEL_HANDLER_PORT}
# echo ${OLLAMA_PORT}
# echo ${OPEN_WEB_UI_PORT}

docker compose -f ${COMPOSE} up