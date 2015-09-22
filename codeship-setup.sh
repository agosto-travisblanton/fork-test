#!/bin/bash --login
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

cd webapp


printf "\n${COLOR_LIGHT_GREEN}===> Installing node packages via npm...${COLOR_OFF}\n"

npm install

