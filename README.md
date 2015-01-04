# Setting up a simple OCR server

### Beginning steps
First, we have to install some shit. As always, configging your
env is 90% of the fun. This is in Ubuntu 14.04 but it should work
for 12.x and 13.x as well. Though I have not tested this. YMMV.

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

Flask Boilerplate is a wonderful library for getting a simple, 
pythonic server running. Check out the repository here:
https://github.com/mjhea0/flask-boilerplate

In the `flask_server` directory I have included the running final version of the server
with a commit for each stage of the operation as we will build it up. The commit for this
is "add flask server v1"

It is commit hash `814980374bd4d7d844ecdc1642d0b31074cd239f`

Now, on to the fun stuff. First, we will need to build a way
to interface with Tesseract using python. We COULD use `popen`
but that just feels ghetto. A very minimal, but functional
python package wrapping Tesseract is `pytesseract`, which is
what we will rely on here.

Now, we need to make a class using pytesseract to intake images, and read them.
Here is the full code, but we will go through it step by step:

```
import logging
import os
import sys
import pdb
import pytesseract

from logging import Formatter, FileHandler
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from nltk.corpus import words
from StringIO import StringIO

_ALL_WORDS = words.words()

class OcrEngine():
    def process_image(self, im):
        """pass an image PIL object in and run basic text analysis"""
        im.filter(ImageFilter.SHARPEN)
        im2 = self.resize_image(im, 5, 5);im2.filter(ImageFilter.SHARPEN)
        im2.save("temp.jpg");image = Image.open('temp.jpg')
        words_by_row = self._get_rows(pytesseract.image_to_string(image))
        return self._format_output([self._check_group(word_group) for word_group in words_by_row])

    def resize_image(self, image, x, y):
        """resize an image passing in x and y axis multipliers"""
        nx, ny = image.size
        return image.resize((int(nx*x), int(ny*y)), Image.BICUBIC)

    def _get_rows(self, string):
        all_words = string.split("\n")
        last_words = []
        for group in all_words:
            last_words.append(group.split(" "))
        return last_words

    def _check_word(self, word):
        if str(word).lower() in _ALL_WORDS:
            return str(word).lower()
        else:
            return ""

    def _check_group(self, word_group):
        final = []
        for word in word_group:
            final.append(self._check_word(word))
        return final
    def _format_output(self, output):
        final = []
        for group in output:
            for item in group:
                good_group = []
                if item != "":
                    good_group.append(item)
            final.append(good_group)
        return final

ENGINE = OcrEngine()

```
Wonderful! A simple class we can use. But let's investigate it further
in order to truly understand the code and why we are doing what this.
