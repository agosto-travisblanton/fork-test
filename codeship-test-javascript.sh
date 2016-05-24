#!/usr/bin/env bash
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'
NODEJS_RUNTIME_VERSION=4.1.1

cd webapp

printf "\n${COLOR_LIGHT_GREEN}===> Sourcing nvm...${COLOR_OFF}\n"
. ~/.nvm/nvm.sh

printf "\n${COLOR_LIGHT_GREEN}===> Installing node runtime via nvm...${COLOR_OFF}\n"
nvm install $NODEJS_RUNTIME_VERSION
nvm use $NODEJS_RUNTIME_VERSION

printf "\n${COLOR_LIGHT_GREEN}===> Installing installing the latest version of bower...${COLOR_OFF}\n"
npm install -g bower@latest

printf "\n${COLOR_LIGHT_GREEN}===> Installing node packages via npm...${COLOR_OFF}\n"
npm install

printf "\n${COLOR_LIGHT_GREEN}===> Installing web packages via bower...${COLOR_OFF}\n"

bower install

printf "\n${COLOR_LIGHT_GREEN}===> Running Jasmine tests in gulp build...${COLOR_OFF}\n"

gulp test
