#!/bin/bash

# Variables used in docker-compose.yml
export TEMP_DIR="/tmp"   # CHANGE ME to desired location 
export DATA_HOST_PATH="/data"   
export NGINX_HOST_CONFIG_PATH="./nginx/default.cloud.conf"

mkdir -p "${TEMP_DIR}"

/opt/docker/start_cloud_helper.sh --docker-path "/opt/docker" --partition-names "HC_Volume_103317681" &

crontab -l 2>/dev/null | sed '/start_cloud.sh/ s/^/#/' | crontab -