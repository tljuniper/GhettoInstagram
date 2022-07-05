#!/usr/bin/env python3

# to execute run `FLASK_APP=main.py FLASK_ENV=DEBUG flask run`
import image_processing
import storage
import os
import tempfile
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
DIRPATH = tempfile.mkdtemp()
EXTENSION = "png"


@app.route("/users/<username>/photos", methods=["GET", "POST"])
def image_upload(username):
    if request.method == "POST":
        print(username)
        f = request.files["file"]
        print(f.filename)
        if f.filename != "":
            tmpFilename = os.path.join(DIRPATH, f.filename)
            f.save(tmpFilename)
            storagePath = storage.getPath(username, EXTENSION)
            image_processing.png_convert(tmpFilename, storagePath)
            return Response(status=200)
        else:
            return Response(status=400)
    return f"""
    <!doctype html>
    <title>{username}: Upload new Photo</title>
    <h1>Hi {username}!</h1>
    <h2>Upload new Photo:</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


@app.route("/feed", methods=["GET"])
def feed():
    user = request.args.get("users")
    return Response(status=200)


@app.route("/")
def index():
    return "This is Vinstagram"


def run():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    run()