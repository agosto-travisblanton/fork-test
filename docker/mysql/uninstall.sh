#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

CONTAINER_NAME='provisioning_mysql'
IMAGE_NAME='agosto/mysql'

printf "\n${COLOR_LIGHT_GREEN}=====> Stopping the '$CONTAINER_NAME' Docker container...${COLOR_OFF}\n"
docker stop $CONTAINER_NAME

printf "\n${COLOR_LIGHT_GREEN}=====> Removing the '$CONTAINER_NAME' Docker container...${COLOR_OFF}\n"
docker rm $CONTAINER_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> Docker container '$CONTAINER_NAME' removed!${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Removing the '$IMAGE_NAME' Docker image...${COLOR_OFF}\n"
docker rmi $IMAGE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> Docker image '$IMAGE_NAME' removed!${COLOR_OFF}\n"



