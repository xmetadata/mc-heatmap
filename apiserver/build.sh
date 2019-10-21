#!/bin/sh

datetime=`date +"%Y%m%d%H%M%S"`

# docker build
docker build -t apiserver:v1.0-${datetime} .

# force change tag :latest
docker tag apiserver:v1.0-${datetime} apiserver
