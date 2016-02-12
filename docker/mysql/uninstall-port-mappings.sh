#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
MAPPED_PORT=3306

printf "\n${COLOR_LIGHT_GREEN}=====> Shutting down docker-machine ...${COLOR_OFF}\n"
docker-machine stop default
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine process has been shut down.${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Removing docker-machine-vm port forwarding for port $MAPPED_PORT ...${COLOR_OFF}\n"
VBoxManage modifyvm "default" --natpf1 delete "tcp-port$MAPPED_PORT";
VBoxManage modifyvm "default" --natpf1 delete "udp-port$MAPPED_PORT";
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine-vm port forwarding for port $MAPPED_PORT has been removed!${COLOR_OFF}\n"

