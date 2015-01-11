# Setting up a Simple OCR Server

**Let's build a simple a simple Flask OCR server with [Tesseract](http://en.wikipedia.org/wiki/Tesseract_%28software%29). *This is a guest post by [Bobby Grayson](http://twitter.com/_devbob), a software developer at [Ahalogy](http://www.ahalogy.com/).***

## Beginning steps

First, we have to install some dependencies. As always, configuring your environment is 90% of the fun.

> This post has been tested on Ubuntu version 14.04 but it should work for 12.x and 13.x versions as well. If you're running OSX, you can use [VirtualBox](http://osxdaily.com/2012/03/27/install-run-ubuntu-linux-virtualbox/) or a droplet on [DigitalOcean](https://www.digitalocean.com/) (recommended!) to create the appropriate environment.

### Downloading dependencies

We need [Tesseract](http://en.wikipedia.org/wiki/Tesseract_%28software%29) and all of its dependencies, which includes [Leptonica](http://www.leptonica.com/), as well as some other packages that power these two for sanity checks to start. Now, I could just give you a list of magic commands that I know work in the env. But, lets explain things a bit first.

> **NOTE**: You can also use the [_run.sh](link) shell script to quickly install the dependencies along with Leptonica and Tesseract and the relevant English language packages. If you go this route, skip down to the [Web-server time!](link) section. But please consider manually building these libraries if you have not before. It is chicken soup for the hacker's soul to play with tarballs and make. However, first are our regular apt-get dependencies (before we get fancy). 

```sh
$ sudo apt-get update
$ sudo apt-get install autoconf automake libtool
$ sudo apt-get install libpng12-dev
$ sudo apt-get install libjpeg62-dev
$ sudo apt-get install g++
$ sudo apt-get install libtiff4-dev
$ sudo apt-get install libopencv-dev libtesseract-dev 
$ sudo apt-get install git 
$ sudo apt-get install cmake 
$ sudo apt-get install build-essential
$ sudo apt-get install libleptonica-dev
$ sudo apt-get install liblog4cplus-dev
$ sudo apt-get install libcurl3-dev
$ sudo apt-get install python2.7-dev
$ sudo apt-get install tk8.5 tcl8.5 tk8.5-dev tcl8.5-dev
$ sudo apt-get build-dep python-imaging --fix-missing
```

We run `sudo apt-get update` is short for 'make sure we have the latest package listings.
`g++` is the GNU compiled collection.
We also get a bunch of libraries that allow us to toy with images. ie `libtiff` `libpng` etc. 
We also get `git`, which if you lack famliiarity with but have found yourself here, you may want to read [The Git Book](link).
Beyond this, we also ensure we have `Python 2.7`, our programming language of choice.
We then get the `python-imaging` library set up for interaction with all these pieces.

Speaking of images: now, we'll need [ImageMagick](http://www.imagemagick.org/) as well if we want to toy with images before we throw them in programmatically, now that we have all the libraries needed to understand and parse them in..

```sh
$ sudo apt-get install imagemagick
```

### Building Leptonica

Now, time for Leptonica, finally! (Unless you ran the shell scripts and for some reason are seeing this. In which case proceed to the [Webserver Time!](link) section. 

```sh
$ wget http://www.leptonica.org/source/leptonica-1.70.tar.gz
$ tar -zxvf leptonica-1.70.tar.gz
$ cd leptonica-1.70/
$ ./autobuild
$ ./configure
$ make
$ sudo make install
$ sudo ldconfig
```

If this is your first time playing with tar, heres what we are doing:

- get the binary for Leptonica (`wget`)
- unzip the tarball  and  (`x` for extract, `v` for verbose...etc. For a detailed explanation: `man tar`)
- `cd` into our new unpacked directory
- run `autobuild` and `configure` bash scripts to set up the application
- use `make` to build it
- install it with `make` after the build
- create necessary links with `ldconfig`

Boom, now we have Leptonica. On to Tesseract!

### Building Tesseract

And now to download and build Tesseract...

```sh
$ cd ..
$ wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.02.tar.gz
$ tar -zxvf tesseract-ocr-3.02.02.tar.gz
$ cd tesseract-ocr/
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
$ sudo ldconfig
```
The process here mirrors the Leptonica one almost perfectly. So for explanation, I'll keep this DRY and just say see above.

We need to set up an environment variable to source our Tesseract data, so we'll take care of that now:

````sh
$ export TESSDATA_PREFIX=/usr/local/share/
```

Now, lets get the Tesseract english language packages that are relevant:

```
$ cd ..
$ wget https://tesseract-ocr.googlecode.com/files/tesseract-ocr-3.02.eng.tar.gz
$ tar -xf tesseract-ocr-3.02.eng.tar.gz
$ sudo cp -r tesseract-ocr/tessdata $TESSDATA_PREFIX
```

BOOM! We now have Tesseract. We can use the CLI. Feel free to read the [docs](https://code.google.com/p/tesseract-ocr/) if you want to play. However, we need a Python wrapper to truly achieve our end goal. So the next step is setting
up a Flask server that will allow us to easily build an API that we will POST requests to with a link to an image, and it will run the character recognition on them.

## Web-server time!

Now, on to the fun stuff. First, we will need to build a way to interface with Tesseract via Python. We COULD use `popen` but that just feels wrong/unPythonic. A very minimal, but functional Python package wrapping Tesseract is [pytesseract](https://github.com/madmaze/pytesseract), which is what we will rely on here.

Before beginning, grab the boilerplate code/structure [here](https://github.com/mjhea0/ocr_tutorial/releases/tag/v0) and setup the project structure on your machine. Make sure to setup a virtualenv and install the requirements via pip.

> **NOTE**: Want to quickly get started? Run the [_app.sh](link) shell script. This will give you a version that has some git tags that can allow us to easily get to ertain points in the exercise. If you are unfamiliar with flask, using the final repository as reference is a solid method to understanding the basics of building a flask server. You can find a great tutorial [here](https://realpython.com/blog/python/kickstarting-flask-on-ubuntu-setup-and-deployment/) as well, specific to Ubuntu.

```sh
$ wget https://github.com/mjhea0/ocr_tutorial/archive/v0.tar.gz
$ tar -xf v0.tar.gz
$ mv ocr_tutorial-0/* ../../home/
$ cd ../../home
$ sudo apt-get install python-virtualenv
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

> **NOTE**: Flask Boilerplate (maintained by [Real Python](https://realpython.com) is a wonderful library for getting a simple, Pythonic server running. We customized this for our base application. Check out the [Flask Boilerplate repository](https://github.com/mjhea0/flask-boilerplate) for more info.

### Let's make an OCR Engine

Now, we need to make a class using pytesseract to intake images, and read them. Create a new file called *ocr.py* in "flask_server" and add the following code:

```python
import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from nltk.corpus import words
from StringIO import StringIO

_ALL_WORDS = words.words() # we'll use it later don't worry


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
```

Wonderful!

So, our main method is `process_image()`, where we sharpen the image to crisp up the text.

Sweet! A working module to toy with. However, we have some maintenance to do in order to get this code to run. If one desires to do any sort of real processing, they best be using quite a bit of [NLTK](http://www.nltk.org/), so we will need to install all corpora.

### Configuring NLTK

> **NOTE** if you would rather not do any analysis of text on the images, you can skip this. But I mean, who doesn't process their strings yo? Let's just do it and not be lazy, boring developers. 

Since the NLTK is in our env (installed via pip), let's run `python` to fire up a shell:

```sh
$ import nltk
$ nltk.download()
$ d
$ all-corpora
```

Grab a beer. This will take a minute. Quit and exit the shell once done. Now, we have everything we need to run some basic OCR.

## Optional: Building a CLI tool for your new OCR Engine

Making a CLI is a great proof of concept, and a fun breather after doing so much configuration. So lets take a stab at making one. Create a new file within "flask_server" called *cli.py* and then add the following code:

```python
import sys
import requests
import pytesseract
from PIL import Image
from nltk.corpus import words
from StringIO import StringIO


_ALL_WORDS = words.words()  # we use this later


def get_image(url):
    return Image.open(StringIO(requests.get(url).content))


if __name__ == '__main__':
    """Tool to test the raw output of pytesseract with a given input URL"""
    sys.stdout.write("""
===OOOO=====CCCCC===RRRRRR=====\n
==OO==OO===CC=======RR===RR====\n
==OO==OO===CC=======RR===RR====\n
==OO==OO===CC=======RRRRRR=====\n
==OO==OO===CC=======RR==RR=====\n
==OO==OO===CC=======RR== RR====\n
===OOOO=====CCCCC===RR====RR===\n\n
""")
    sys.stdout.write("A simple OCR utility\n")
    url = raw_input("What is the url of the image you would like to analyze?\n")
    image = get_image(url)
    sys.stdout.write("The raw output from tesseract with no processing is:\n\n")
    sys.stdout.write("-----------------BEGIN-----------------\n")
    sys.stdout.write(pytesseract.image_to_string(image) + "\n")
    sys.stdout.write("------------------END------------------\n")
```

This is really quite simple. Line by line we look at the text output from our engine, and output it to STDOUT. Test it out (`python flask_server/cli.py`) with a few image urls, or play with your own ascii art for a good time.

## Back to the server

Now that we have an engine, we need to get ourselves some output! Add the following route handler and view function to *app.py*:

```python
@app.route('/ocr', methods=["POST"])
def ocr():
    try:
        url = request.form['image_url']
        output = process_image(url)
        return jsonify({"output": output})
    except KeyError:
        return jsonify({"error": "Did you mean to send data formatted: '{"image_url": "some_url"}'")
```

Make sure to update the imports:

```python
import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify

from ocr import process_image
```

Now, as you can see, we just add in the JSON response of the Engine's `process_image()` method, passing it in a file object using `Image` from PIL to install.

> **NOTE**: You will not have `PIL` itself installed; this runs off of `Pillow` and allows us to do the same thing. This is because the PIL library was at one time forked, and turned into `Pillow`. The community has strong opinions on this matter. Consult google for insight and drama.

## Let's test!

Run your app:

```sh
$ cd flask_server/
$ python app.py
```

Then in another terminal tab run:

```sh
$ curl -X POST http://localhost:5000/ocr -d "{'image_url': 'some_url'}"
```

### Example

```sh
$ curl -X POST http://localhost:5000/ocr -d 'https://s-media-cache-ec0.pinimg.com/originals/02/58/8f/02588f420dd4fe0ed13d93613de0da7.jpg'
{
  "output": "Stfawfbeffy Lemon\nHerbal Tea\nSlushie"
}
```

### Optimize text with NLTK?

## Conclusion and next steps

This is a WIP and I plan on maintaining and adding to it. Each piece will add more to the main tutorial. Hope you enjoyed. Please fork or star if you want to see/do/use. Grab the final code [here](https://github.com/mjhea0/ocr_tutorial/releases/tag/v1) from the [repository](https://github.com/mjhea0/ocr_tutorial). Cheers!

:)
