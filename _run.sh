#!/bin/sh

# Install Dependencies
sudo apt-get update
sudo apt-get install -y autoconf automake libtool
sudo apt-get install -y libpng12-dev
sudo apt-get install -y libjpeg62-dev
sudo apt-get install -y g++
sudo apt-get install -y libtiff4-dev
sudo apt-get install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install -y liblog4cplus-dev libcurl3-dev
sudo apt-get install -y python2.7-dev tk8.5 tcl8.5 tk8.5-dev tcl8.5-dev
sudo apt-get build-dep -y python-imaging --fix-missing
sudo apt-get install -y imagemagick


# Building Leptonica
wget http://www.leptonica.org/source/leptonica-1.70.tar.gz
tar -zxvf leptonica-1.70.tar.gz
cd leptonica-1.70/
./autobuild
./configure
make
sudo make install
sudo ldconfig

# Building Tesseract
cd ..
wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
tar -zxvf tesseract-ocr-3.02.02.tar.gz
cd tesseract-ocr/
./autogen.sh
./configure
make
sudo make install
sudo ldconfig

# Set Environment Variable
TESSDATA_PREFIX=/usr/local/share/

# Download the relevant Tesseract English Language Packages
cd ..
wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz
tar -xf tesseract-ocr-3.02.eng.tar.gz
sudo cp -r tesseract-ocr/tessdata $TESSDATA_PREFIX
