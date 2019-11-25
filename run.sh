#!/bin/sh

# Shell script for building / configuring the environment to run commands
# answering the Compass data challenge.
#
# Assumptions:
#   - Docker is installed, and available as $(which docker)
#   - Git is installed, and available as $(which git)
#   - Repository .git/ directory is intact and referenceable

DOCKER=$(which docker)
GIT=$(which git)

GIT_REPO_ROOT=$(git rev-parse --show-toplevel)
DOCKER_BASE_IMAGE='continuumio/anaconda3:latest'
DOCKER_IMAGE_NAME='compass:latest'
DOCKER_CONTAINER_NAME='compass_data_challenge'

$DOCKER pull $DOCKER_BASE_IMAGE

$DOCKER build $GIT_REPO_ROOT \
    --tag $DOCKER_IMAGE_NAME

CONTAINER_EXISTS=$($DOCKER ps -a --format '{{.Names}}' --filter name=$DOCKER_CONTAINER_NAME)

if [ -n "$CONTAINER_EXISTS" ];
then
    $DOCKER stop $DOCKER_CONTAINER_NAME && $DOCKER rm $DOCKER_CONTAINER_NAME;
fi

$DOCKER run \
    --name $DOCKER_CONTAINER_NAME \
    --network=host \
    -it $DOCKER_IMAGE_NAME
