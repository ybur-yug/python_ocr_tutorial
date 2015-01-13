# Docker OSX Install

Build the container and run the image...

```sh
$ boot2docker init
$ boot2docker start
$ docker build --rm -t flask-docker-ocr .
$ docker run -p 80:5000 flask-docker-ocr
```