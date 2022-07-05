#!/usr/bin/env python3

# to execute run `FLASK_APP=main.py FLASK_ENV=DEBUG flask run`
from PIL import Image
import os
import tempfile
from datetime import datetime
import uuid
from flask import Flask
from flask import request, url_for
from flask import Response
from os.path import join, basename
from os import listdir

STORAGE = os.getenv("STORAGE_DIR")
SIZE = 1000
app = Flask(__name__, static_url_path="/static", static_folder=STORAGE)
DIRPATH = tempfile.mkdtemp()
EXTENSION = ".png"


def generateUniquePath(pathname, extension):
    uniqueFilepath = pathname + "-" + str(uuid.uuid4()) + extension
    if os.path.exists(uniqueFilepath):
        return generateUniquePath(pathname, extension)
    return uniqueFilepath


def getPath(user, extension):
    userPath = os.path.join(STORAGE, user)
    userExists = os.path.exists(userPath)

    if not userExists:
        os.makedirs(userPath)

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S-%f")

    photoPath = os.path.join(userPath, timestampStr)

    uniquePath = generateUniquePath(photoPath, extension)

    return uniquePath


def png_convert(inPath, outPath):
    with Image.open(inPath) as im:
        print()
        print(im.getbbox())

        (_, _, width, height) = im.getbbox()
        print(f"width: {width}")
        print(f"height: {height}")

        half = SIZE / 2

        # New corners for cropped image
        # See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#coordinate-system
        # (0, 0) is the upper left corner
        left = max(0, int((width / 2) - half))
        upper = max(0, int((height / 2) - half))
        right = min(width, int((width / 2) + half))
        lower = min(height, int((height / 2) + half))

        print(f"left: {left}, upper: {upper}, right: {right}, lower: {lower}")

        im = im.crop((left, upper, right, lower))

        # Resize in case image is too small
        im = im.resize((SIZE, SIZE))

        # Convert to black and white
        im = im.convert("L")

        im.save(outPath)


@app.route("/users/<username>/photos", methods=["GET", "POST"])
def image_upload(username):
    if request.method == "POST":
        print(username)
        f = request.files["file"]
        print(f.filename)
        if f.filename != "":
            tmpFilename = os.path.join(DIRPATH, f.filename)
            f.save(tmpFilename)
            storagePath = getPath(username, EXTENSION)
            png_convert(tmpFilename, storagePath)
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

    folders = request.args.get("users").split(",")
    allImages = []
    for folder in folders:
        allImages += map(
            lambda image: join(folder, image), listdir(join(STORAGE, folder))
        )

    allImagesSorted = sorted(allImages, key=lambda path: basename(path), reverse=True)
    urls = map(lambda im: url_for("static", filename=im), allImagesSorted)
    htmlList = map(lambda url: f'<img src="{url}" alt="feed image">', urls)
    html = "-".join(htmlList)
    return html


@app.route("/")
def index():
    return "This is Vinstagram"


def run():
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    run()
