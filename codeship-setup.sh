#!/bin/bash
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

printf "\n${COLOR_LIGHT_GREEN}===> Sourcing nvm...${COLOR_OFF}\n"

. ~/.nvm/nvm.sh


cd ~/src/bitbucket.org/agosto_administrator/skykit-display-device

printf "\n${COLOR_LIGHT_GREEN}===> Installing Python packages via pip...${COLOR_OFF}\n"

pip install PyOpenSSL
pip install py

cd ~/src/bitbucket.org/agosto_administrator/skykit-display-device/webapp

printf "\n${COLOR_LIGHT_GREEN}===> Installing node runtime via nvm...${COLOR_OFF}\n"

nvm install
nvm use

printf "\n${COLOR_LIGHT_GREEN}===> Installing installing the latest version of npm...${COLOR_OFF}\n"

npm install -g npm@latest

printf "\n${COLOR_LIGHT_GREEN}===> Installing installing the latest version of bower...${COLOR_OFF}\n"

npm install -g bower@latest

printf "\n${COLOR_LIGHT_GREEN}===> Installing node packages via npm...${COLOR_OFF}\n"

npm install

printf "\n${COLOR_LIGHT_GREEN}===> Installing web packages via bower...${COLOR_OFF}\n"

bower install
