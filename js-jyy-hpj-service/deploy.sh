#!/usr/bin/bash

images=$1
docker stop post_project && docker rm post_project
docker rmi $images

docker build -t $images .

docker run \
    --restart=always \
    --log-opt max-size=10m \
    --net=host \
    --privileged=true  \
    --name post_project \
    -p 8080:8080 \
    -v /data/front:/usr/src/app/app/front \
    -v /etc/localtime:/etc/localtime \
    -d $images
