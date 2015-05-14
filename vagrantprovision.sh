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

# edit the etc/hosts file to avoid the loopback created on 127.0.0.1 due to virutal box using it
cp /etc/hosts /tmp/hosts.orig
echo "0.0.0.0  localhost" > /tmp/hosts.new
grep -v "127.0.0.1" /etc/hosts >> /tmp/hosts.new
cp /tmp/hosts.new /etc/hosts

#update path
echo "export PATH=$PATH:/usr/google_appengine/:/usr/bin/env" > /etc/profile.d/gae_setup.sh
echo "Install complete"