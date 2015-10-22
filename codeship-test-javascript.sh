#!/usr/bin/env bash
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

cd ~/src/bitbucket.org/administrator/skykit-display-device/webapp

printf "\n${COLOR_LIGHT_GREEN}===> Running Jasmine tests in gulp build...${COLOR_OFF}\n"

gulp test
