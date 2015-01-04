import logging
import requests
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

def get_image(url):
    return Image.open(StringIO(requests.get(url).content))

def process_image(url):
    image = get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return image
