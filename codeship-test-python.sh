#!/usr/bin/env bash
set -e

COLOR_LIGHT_GREEN='\033[1;32m'
COLOR_OFF='\033[0m'



printf "\n${COLOR_LIGHT_GREEN}===> Installing Python packages via pip...${COLOR_OFF}\n"
pip install PyOpenSSL
pip install py
pip install -r requirements.txt

printf "\n${COLOR_LIGHT_GREEN}===> Configuring AppEngine SDK environment...${COLOR_OFF}\n"

export APPENGINE_SDK=/home/rof/appengine/python_appengine

printf "\n${COLOR_LIGHT_GREEN}===> Running Python tests...${COLOR_OFF}\n"

./manage.py pytest --cov-report=term --cov-report=html --cov=. tests/
