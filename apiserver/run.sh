#!/bin/sh

docker stop apiserver
docker rm apiserver

# docker run
docker run -d -p 65534:5050 -v /root/apps/heatmap/apiserver:/src -v /var/log/apiserver:/src/log --restart=always --name=apiserver apiserver
