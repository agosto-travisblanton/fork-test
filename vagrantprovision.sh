#!/bin/sh

echo "Set sensible OS env defaults ..."
locale-gen en_US.UTF-8
update-locale LANG=en_US.UTF-8

# General update
sudo apt-get -y update

# Zipping utilities
sudo apt-get -y install zip unzip

echo "Install OS dependencies ..."
apt-get update && apt-get install -y python-dev libpq-dev libjpeg8 libjpeg62-dev git python-software-properties

echo "Install phantomjs"
sudo apt-get install -y build-essential g++ flex bison gperf ruby perl \
  libsqlite3-dev libfontconfig1-dev libicu-dev libfreetype6 libssl-dev libpng-dev libjpeg-dev

# Install Node & npm then update npm
echo "Installing nodejs..."
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo apt-get -y install nodejs
sudo apt-get -y install npm
sudo npm install npm -g

echo "Installing nvm to manage node versions..."
cd /workspace

mkdir /workspace/.nvm
export NVM_DIR="/workspace/.nvm"

# Installing nvm
wget -qO- https://raw.github.com/creationix/nvm/master/install.sh | sh

# This enables NVM without a logout/login
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
nvm install stable

sudo npm install -g phantomjs

echo "Running apt-get update ..."
apt-get update

echo "Install PIP  ..."
# Github doesn't send a last modified header so wget cache doesn't work
if [ ! -f /var/cache/wget/get-pip.py ]; then
    wget  -N -P /var/cache/wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
fi
cp /var/cache/wget/get-pip.py /home/vagrant/get-pip.py
cd /home/vagrant
python get-pip.py

# install Google Appengine SDK
wget -nv https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.20.zip -O google_appengine.zip && unzip -q google_appengine.zip; rm google_appengine.zip
mv google_appengine /usr

pip install --download=/tmp -r /vagrant/requirements.txt
pip install --use-wheel --no-index --find-links=/tmp --exists-action=b -r /vagrant/requirements.txt

# edit the etc/hosts file to avoid the loopback created on 127.0.0.1 due to virutal box using it
cp /etc/hosts /tmp/hosts.orig
echo "0.0.0.0  localhost" > /tmp/hosts.new
grep -v "127.0.0.1" /etc/hosts >> /tmp/hosts.new
cp /tmp/hosts.new /etc/hosts

# update path
echo "export PATH=$PATH:/usr/google_appengine/:/usr/bin/env" > /etc/profile.d/gae_setup.sh
echo "export APPENGINE_SDK=/usr/google_appengine" >>/etc/profile.d/gae_setup.sh
echo "Install complete"