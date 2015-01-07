import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from nltk.corpus import words
from StringIO import StringIO

_ALL_WORDS = words.words()


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image)


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
