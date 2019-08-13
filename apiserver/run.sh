#!/bin/sh

docker stop apiserver
docker rm apiserver

# docker run
docker run -d -p 5050:5050 -v /var/log/apiserver:/src/log --restart=always --name=apiserver apiserver
