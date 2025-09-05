#!/bin/bash

# Usage: ./start_cloud.sh --ip <FLOATING_IP> --partition-names "<PARTITION_NAME_1> <PARTITION_NAME_2> ..." --docker-path <PATH_TO_DOCKER_COMPOSE>
# Example: ./start_cloud.sh --ip "5.161.21.191" --partition-names "HC_Volume_102861833 HC_Volume_102894653" --docker-path "/opt/docker"


: '
This script executes required instance setup logic at intervals of a minute based on the flags specified. 
- If floating ip is specified, it will add the floating ip to the network interface eth0
- If partition names are specified, it will wait until one of the specified external volumes is attached and then mount it
-- It will also export the path to the mounted volume as PARTITION_PATH in /opt/shared_env.sh
- It will then start up the docker containers in the specified path using docker-compose
'

exec > >(tee -a /var/log/start_cloud_helper.log) 2>&1

while [[ $# -gt 0 ]]; do
    case $1 in 
        --ip)
            FLOATING_IP="$2"
            shift 2
            ;;
        --partition-names)
            PARTITION_NAMES="$2"
            shift 2
            ;;
        --docker-path)
            DOCKER_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

export PARTITION_PATH=""

if [[ -z "$DOCKER_PATH" ]]; then
    echo "Error: Missing required arguments. Please provide at least --docker-path."
    exit 1
fi

PARTITION_ADDED=1
FLOATING_IP_ADDED=1

if [[ -n "$PARTITION_NAMES" ]]; then
    echo "Partition names specified, will mount attached external volume before starting containers..."
    PARTITION_ADDED=0
fi

if [[ -n "$FLOATING_IP" ]]; then
    echo "Floating IP specified, will add to network interface eth0 before starting containers..."
    FLOATING_IP_ADDED=0
fi

while true; do
    if [[ -n PARTITION_NAMES ]]; then
        echo "Checking for external volumes: ${PARTITION_NAMES}"

        for pdir in ${PARTITION_NAMES}; do
            cur_local_path="/mnt/${pdir}"
            cur_external_path="/dev/disk/by-id/scsi-0${pdir}"

            if [[ -e "$cur_external_path" ]]; then
                echo "[${pdir}] Required external volume attached, attempting to mount..."
                mkdir -p "$cur_local_path"
                mount -o discard,defaults "$cur_external_path" "$cur_local_path"

                echo "export PARTITION_PATH=${cur_local_path}" > /opt/shared_env.sh  # For future scripts that need partition path

                chmod +x /opt/shared_env.sh
                source /opt/shared_env.sh
                
                PARTITION_ADDED=1
                break
            fi
        done
    fi

    if [[ -n "$FLOATING_IP" ]] && ! ip addr show dev eth0 | grep -q "$FLOATING_IP"; then
        echo "Floating ip ${FLOATING_IP} has not been added to network interface eth0, doing so now..."
        ip addr add "$FLOATING_IP" dev eth0

        FLOATING_IP_ADDED=1
    fi


   if [[ "$PARTITION_ADDED" -eq 1 && "$FLOATING_IP_ADDED" -eq 1 ]]; then
        echo "Setup complete, ready to start containers!"
        break
    fi
    
    echo "Setup not complete, sleeping for 60 seconds before trying again..."
    sleep 60
done


cd "$DOCKER_PATH" || exit 1
docker-compose down
docker-compose build
docker-compose up -d

echo "containers started up successfully!"
