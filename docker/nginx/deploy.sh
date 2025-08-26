#!/bin/bash

exec > >(tee -a /var/log/container-nginx/container-nginx.log) 2>&1

apt update

# apt install -y certbot python3-certbot-nginx
apt install -y vim

cp /opt/nginx.conf /etc/nginx/nginx.conf

rm -rf /data/*

cp -r /opt/temp_external/books/project_hail_mary/project_hail_mary_text/section_3/* /data/

cp -r /opt/temp_external/posts/section_3/post_3.json /data/posts.json

nginx -g "daemon off;"