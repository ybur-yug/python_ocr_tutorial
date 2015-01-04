import pdb
import logging
import urllib
import pdb
import os
import sys

from forms import *
from PIL import Image
from logging import Formatter, FileHandler
from flask import Flask, render_template, request, jsonify
from ocr import ENGINE

app = Flask(__name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/ocr', methods=["POST"])
def ocr():
    image_url = request.form.keys()[0]
    image = urllib.urlretrieve(image_url, 'temp.jpg')
    image = Image.open('temp.jpg')
    return jsonify({"words":ENGINE.process_image(image)})


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
