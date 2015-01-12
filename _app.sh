#!/bin/sh

# Setup App
wget https://github.com/rhgraysonii/ocr_tutorial/archive/v0.tar.gz
tar -xf v0.tar.gz
mv ocr_tutorial-0/* ../home/
cd ../home
sudo apt-get install -y python-virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
