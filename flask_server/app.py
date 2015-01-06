import os
import logging
from logging import Formatter, FileHandler
from flask import Flask, request, jsonify

from ocr import process_image


app = Flask(__name__)


@app.route('/ocr', methods=["POST"])
def ocr():
    try:
        url = request.form.keys()[0]
        output = process_image(url)
        return jsonify({"output": output})
    except:
        return jsonify({"error": "Did you send the proper url?"})


@app.errorhandler(500)
def internal_error(error):
    print str(error)


@app.errorhandler(404)
def not_found_error(error):
    print str(error)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: \
            %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
