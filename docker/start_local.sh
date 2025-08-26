#!/bin/bash

# Script to deploy youtube downloader containers locally (For amd based architecture systems bc needs a diff ffmpeg)

# Variables used in docker-compose.yml
export TEMP_DIR="/Users/andrechang/TEMP"   # CHANGE ME to desired location 
export APP_ENV="local"
export DATA_HOST_PATH="${TEMP_DIR}/data"   
export FFMPEG_HOST_PATH="${TEMP_DIR}/bin"  
export NGINX_HOST_CONFIG_PATH="./nginx/default.local.conf"
export HOST_ENDPOINT="http://127.0.0.1"

mkdir -p "${TEMP_DIR}"

docker-compose down
docker-compose build
docker-compose up -d
