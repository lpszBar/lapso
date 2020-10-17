#!/bin/sh

docker stop lapso 2> /dev/null ||  \
mkdir -p /opt/lapso-db && \
touch /opt/lapso-db/lapso.db && \
docker pull abelgvidal/lapso && \
docker run --rm -it \
           --name=lapso \
           -d \
           -p 80:80 \
           -v=/opt/lapso-db/lapso.db:/app/db/lapso.db \
           abelgvidal/lapso:latest