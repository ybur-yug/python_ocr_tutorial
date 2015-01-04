### To Run

`virtualenv . && source bin/activate`

`pip install -r requirements.txt`

Have Tesseract and Leptonica configured.

`python app.py`

POST to port 5000 in the format:

`curl -X POST http://localhost:5000/ocr -d 'image_url'`

# Happy Hacking

