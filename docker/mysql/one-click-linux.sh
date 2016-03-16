#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
MAPPED_PORT=3306
MACHINE_NAME=agosto
CONTAINER_NAME=provisioning_mysql
IMAGE_NAME=agosto/mysql

# BUILD IMAGE
printf "\n${COLOR_LIGHT_GREEN}=====> Building the Docker image: '$IMAGE_NAME' ...${COLOR_OFF}\n"
docker build -t $IMAGE_NAME .
printf "\n${COLOR_LIGHT_GREEN}=====> Creating the Docker container: '$CONTAINER_NAME' from image: '$IMAGE_NAME'...${COLOR_OFF}\n"

# BUILD CONTAINER
docker create -p $MAPPED_PORT:3306 -P --name $CONTAINER_NAME $IMAGE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> Docker container '$CONTAINER_NAME' listening on port $MAPPED_PORT.${COLOR_OFF}\n"

# START CONTAINER
docker start $CONTAINER_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> Docker container '$CONTAINER_NAME' started on $MAPPED_PORT"
