#!/bin/bash

exec > >(tee -a /var/log/container-nginx/container-nginx.log) 2>&1

apt update

# apt install -y certbot python3-certbot-nginx
apt install -y vim

cp /opt/nginx.conf /etc/nginx/nginx.conf

mkdir -p /webapp

cp -r /opt/external_volume/webapp/* /webapp/

source /opt/external_volume/.env

python3 /opt/update.py --transfer-only

nginx -g "daemon off;"