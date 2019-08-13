#!/bin/sh

datetime=`date +"%Y%m%d%H%M%S"`

# docker build
docker build -t apiserver:${datetime} .

# force change tag :latest
docker tag apiserver:${datetime} apiserver
