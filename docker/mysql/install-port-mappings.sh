#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
MAPPED_PORT=3306
MACHINE_NAME=agosto

printf "\n${COLOR_LIGHT_GREEN}=====> Shutting down docker-machine $MACHINE_NAME...${COLOR_OFF}\n"
docker-machine stop $MACHINE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine $MACHINE_NAME process has been shut down.${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Configuring docker-machine-vm $MACHINE_NAME port forwarding for port $MAPPED_PORT ...${COLOR_OFF}\n"
VBoxManage modifyvm "$MACHINE_NAME" --natpf1 "tcp-port$MAPPED_PORT,tcp,,$MAPPED_PORT,,$MAPPED_PORT";
VBoxManage modifyvm "$MACHINE_NAME" --natpf1 "udp-port$MAPPED_PORT,udp,,$MAPPED_PORT,,$MAPPED_PORT";
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine-vm $MACHINE_NAME port forwarding for port $MAPPED_PORT has been configured!${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Starting up docker-machine $MACHINE_NAME ...${COLOR_OFF}\n"
docker-machine start $MACHINE_NAME
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine $MACHINE_NAME process has been started!${COLOR_OFF}\n"



