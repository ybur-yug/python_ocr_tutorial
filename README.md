# Setting up a simple OCR server

### Beginning steps
First, we have to install some shit. As always, configging your
env is 90% of the fun. This is in Ubuntu 14.04 but it should work
for 12.x and 13.x as well. Though I have not tested this. YMMV.
OSX is a shot in the dark. glhf.

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

### Building Leptonica
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

### Building Tesseract
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

### Webserver time!
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

### Lets make an OCR Engine
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

    # FIXME use fucking comprehensions and map
    def _get_rows(self, string):
        all_words = string.split("\n")
        last_words = []
        for group in all_words:
            last_words.append(group.split(" "))
        return last_words

    def _check_word(self, word):
        return str(word).lower() if str(word).lower() in _ALL_WORDS else ""

    # FIXME use fucking comprehensions and map
    def _check_group(self, word_group):
        final = []
        for word in word_group:
            final.append(self._check_word(word))
        return final

    # FIXME use fucking comprehensions and map
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
A note:
I know a lot of this code needs some maps, filters, list comprehensions,
and other pythonic love. I scrapped this together quite quickly and welcome
a PR of some cleanup. I will do it myself in the future when I've the time
if not. Going on...

Wonderful! A simple class we can use. But let's investigate it further
in order to truly understand the code and why we are doing what this.

Our main method is `process_image`. Let's dig into it.

`im.filter(ImageFilter.SHARPEN)`

First, we sharpen the image. This will crisp up the text. 
Next, we go in and blow it up, and sharpen again.

`im2 = self.resize_image(im, 5, 5);im2.filter(ImageFilter.SHARPEN)`

and now we use some private methods to get the text out, but we have our output

`words_by_row = self._get_rows(pytesseract.image_to_string(image))`

Sweet! A working module to toy with. However, we have some maintenance to do 
in order to get this code to run. We are using quite a bit of nltk. So, we
will need to install all corpora.

from the main directory of the flask server, we need to make a virtualenv

`virtualenv .`

`source bin/activate`

Now lets install everything.

`pip install -r requirements.txt`

### Configuring NLTK
And now that NLTK will be in our env, we run `python` to fire up a shell.

In this, we are going to run the following:

```
import nltk
nltk.download()
d
all-corpora
```
Grab a beer. This will take a minute.

Now, we have everything we need to run some basic OCR.

### Optional: Building a CLI tool for your new OCR Engine
Making a CLI is a great proof of concept, and a fun breather
after doing so much configuration. So lets take a stab at making
one.

```
import os
import sys
import pdb
import requests
import pytesseract

from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from nltk.corpus import words
from StringIO import StringIO

_ALL_WORDS = words.words()

def get_image(url):
    return Image.open(StringIO(requests.get(url).content))

if __name__ == '__main__':
    """This is a tool to test the raw output of pytesseract with a given input URL"""
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
    sys.stdout.write("The raw output from tesseract with no processing is:\n\n\n")
    sys.stdout.write("-----------------BEGIN-----------------\n")
    sys.stdout.write(pytesseract.image_to_string(image) + "\n")
    sys.stdout.write("------------------END------------------\n")
```

This is really quite simple. Line by line we look at the text output
from our engine, and output to to STDOUT. Test it out with a few image
urls, or play with your own ascii art for a good time.

### Back to the server
Now, we have an engine, we have an API, and we need to get ourselves some
output!

Lets go back to our method for outputting Engine reads:

```
@app.route('/ocr', methods=["POST"])
def ocr():
    image_url = request.form.keys()[0]
    image = urllib.urlretrieve(image_url, 'temp.jpg')
    image = Image.open('temp.jpg')
    return jsonify({"words":ENGINE.process_image(image)})
```

Now, as you can see, we just add in the JSON response of the Engine's
`process_image` method, passing it in a file object using Image from
PIL to install. A note: You will not have PIL itself installed, this
runs off of `Pillow` but allows us to do the same thing w/that import.

### Possible problems
- Leptonica/Tesseract build issues.
If the versions provided here do not work or are deprecated,
uninstall and the first try installing with `apt-get`.

`sudo apt-get install tesseract-ocr`

If you get an error like:
"some index out of range" on line 512 of some obscure file,
everything crashes, and sets itself on fire (literally),
everything crashes, and sets itself on fire (figuratively),
or the machine spits in your face.

Your best bet is to uninstall/reinstall and compile from the latest
binary you can find, rather than what I have used here. There are many
small configuration issues that may come along, and I would love
to document all of them. So PR's that do this are welcome and I
am working on doing this on different systems myself.

This is a WIP and I plan on maintaining and adding to it. Each
piece will add more to the main tutorial.

Hope you enjoyed, please fork or star if you want to see/do/use
more :)

