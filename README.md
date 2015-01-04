# Setting up a simple OCR server

### Beginning steps
First, we have to install some shit. As always, configging your
env is 90% of the fun

We need Tesseract and Leptonica, as well as some dependencies
for sanity checks to start.

```
sudo apt-get install autoconf automake libtool
sudo apt-get install libpng12-dev
sudo apt-get install libjpeg62-dev
sudo apt-get install libtiff4-dev
sudo apt-get install g++kj
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install liblog4cplus-dev libcurl3-dev
```

Now, we'll need ImageMagick as well if we want to toy with images before we throw them in.

`sudo apt-get install imagemagick`

Now, time for Leptonica, finally!

```
wget http://www.leptonica.org/source/leptonica-1.70.tar.gz
tar -zxvf leptonica-1.70.tar.gz
cd leptonica-1.70/
./autobuild
./configure
make
sudo make install
sudo ldconfig
```

Boom, now we have Leptonica. On to Tesseract!

First, lets go back a dir from here where we have built Leptonica

`cd ..`

And now to download, and build Tesseract

```
wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
tar -zxvf tesseract-ocr-3.02.02.tar.gz 
cd tesseract-ocr/
./autogen.sh 
./configure
make
sudo make install
sudo ldconfig
```

We need to set up an env var to source for our Tesseract data, so we'll take care of that now

`export TESSDATA_PREFIX=/usr/local/share/`

I put it in my `~/.dev_env` file and `source ~/.dev_env` but running the command works too

Now, lets get the Tesseract english language packages that are relevent

```
cd ..
wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz
tar -xf tesseract-ocr-3.02.eng.tar.gz
sudo cp -r tesseract-ocr/tessdata $TESSDATA_PREFIX
```

BOOM! We now have Tesseract. We can use the CLI, and feel free
to read the docs if you want to play. But the next step is setting
up a Flask server that will allow us to easily build an API that
we will POST requests to with a link to an image, and it will
run the character recognition on them.
