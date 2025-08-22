#!/bin/bash

exec > >(tee -a /var/log/container-nginx/container-nginx.log) 2>&1

apt update

# apt install -y certbot python3-certbot-nginx

cp /opt/nginx.conf /etc/nginx/nginx.conf

rm -rf /texts/*

cp -r /opt/temp_external/books/project_hail_mary/project_hail_mary_text/section_4/* /texts/

nginx -g "daemon off;"