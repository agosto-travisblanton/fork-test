#!/bin/bash --login

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

NODE_VERSION=4.1.0

cd webapp

printf "\n${COLOR_LIGHT_GREEN}===> Installing node.js ${NODE_VERSION} via nvm...${COLOR_OFF}\n"
nvm install $NODE_VERSION

printf "\n${COLOR_LIGHT_GREEN}===> Updating npm to the latest...${COLOR_OFF}\n"
npm install -g npm@latest