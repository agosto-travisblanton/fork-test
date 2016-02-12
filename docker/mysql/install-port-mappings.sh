#!/bin/sh

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
MAPPED_PORT=3306

printf "\n${COLOR_LIGHT_GREEN}=====> Shutting down docker-machine ...${COLOR_OFF}\n"
docker-machine stop default
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine process has been shut down.${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Configuring docker-machine-vm port forwarding for port $MAPPED_PORT ...${COLOR_OFF}\n"
VBoxManage modifyvm "default" --natpf1 "tcp-port$MAPPED_PORT,tcp,,$MAPPED_PORT,,$MAPPED_PORT";
VBoxManage modifyvm "default" --natpf1 "udp-port$MAPPED_PORT,udp,,$MAPPED_PORT,,$MAPPED_PORT";
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine-vm port forwarding for port $MAPPED_PORT has been configured!${COLOR_OFF}\n"

printf "\n${COLOR_LIGHT_GREEN}=====> Starting up docker-machine ...${COLOR_OFF}\n"
docker-machine start default
printf "\n${COLOR_LIGHT_GREEN}=====> The docker-machine process has been started!${COLOR_OFF}\n"



