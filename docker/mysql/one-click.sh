#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
MAPPED_PORT=3306
MACHINE_NAME=agosto
CONTAINER_NAME=provisioning_mysql
IMAGE_NAME=agosto/mysql

#### ONLY FOR MAC
#####################################################
# CREATE MACHINE
printf "\n${COLOR_LIGHT_GREEN}=====> Creating docker-machine $MACHINE_NAME...${COLOR_OFF}\n"
docker-machine create -d virtualbox $MACHINE_NAME;

# SET CLIENT
printf "\n${COLOR_LIGHT_GREEN}=====> Set docker client to docker-machine $MACHINE_NAME...${COLOR_OFF}\n"
eval "$(docker-machine env $MACHINE_NAME)"

# SHUT DOWN MACHINE
printf "\n${COLOR_LIGHT_GREEN}=====> Shutting down docker-machine $MACHINE_NAME...${COLOR_OFF}\n"
docker-machine stop $MACHINE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine $MACHINE_NAME process has been shut down.${COLOR_OFF}\n"

# CONFIGURE PORT MAPPINGS
printf "\n${COLOR_LIGHT_GREEN}=====> Configuring docker-machine-vm $MACHINE_NAME port forwarding for port $MAPPED_PORT ...${COLOR_OFF}\n"
VBoxManage modifyvm "$MACHINE_NAME" --natpf1 "tcp-port$MAPPED_PORT,tcp,127.0.0.1,$MAPPED_PORT,,$MAPPED_PORT";
VBoxManage modifyvm "$MACHINE_NAME" --natpf1 "udp-port$MAPPED_PORT,udp,127.0.0.1,$MAPPED_PORT,,$MAPPED_PORT";
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine-vm $MACHINE_NAME port forwarding for port $MAPPED_PORT has been configured!${COLOR_OFF}\n"

# START MACHINE
printf "\n${COLOR_LIGHT_GREEN}=====> Starting up docker-machine $MACHINE_NAME ...${COLOR_OFF}\n"
docker-machine start $MACHINE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine $MACHINE_NAME process has been started!${COLOR_OFF}\n"
#####################################################

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
