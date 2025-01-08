#!/bin/bash

# Store the utilities
FILE=$(realpath "$0")
ROOT=$(dirname "${FILE}")

# Basic Parameters
COMPOSE="${ROOT}/docker-compose.yml"

docker compose -f ${COMPOSE} down