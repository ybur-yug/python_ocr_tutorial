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
