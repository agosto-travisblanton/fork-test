#!/usr/bin/env bash
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'

printf "\n${COLOR_LIGHT_GREEN}===> Configuring AppEngine SDK environment...${COLOR_OFF}\n"

export APPENGINE_SDK=/home/rof/appengine/python_appengine

cd ~/src/bitbucket.org/agosto/skykit-display-device


printf "\n${COLOR_LIGHT_GREEN}===> Running Python tests...${COLOR_OFF}\n"

python manage.py test