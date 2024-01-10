#!/bin/bash

# update and upgrade
cd ~

sudo apt-get -qq -y update
sudo apt upgrade

# install nginx
sudo apt-get install nginx

# Install Chromium
sudo apt install -y chromium

# Install graphviz
sudo apt install -y graphviz graphviz-dev

# Install Node
sudo apt install -y nodejs

# Npm install dependencies
cd /home/sysadmin/sprint-1/scraper
npm install

# Install python3.9
cd ~
sudo apt install -yy python3.9

# Install pip dependencies
cd /home/sysadmin/sprint-1/search
pip3 install -r requirements.txt | grep -v 'Requirement already satisfied'





