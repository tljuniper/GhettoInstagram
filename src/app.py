#!/usr/bin/env python3

# to execute run `FLASK_APP=main.py FLASK_ENV=DEBUG flask run`
from PIL import Image
import os
import tempfile
import os
from datetime import datetime
import uuid
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
DIRPATH = tempfile.mkdtemp()
EXTENSION = ".png"
CWD = os.path.abspath(os.getcwd())
STORAGE = os.path.join(CWD, "storage")
SIZE = 1000


def generateUniquePath(pathname, extension):
    uniqueFilepath = pathname + str(uuid.uuid4()) + extension
    if os.path.exists(uniqueFilepath):
        return generateUniquePath(pathname, extension)
    return uniqueFilepath


def getPath(user, extension):
    userPath = os.path.join(STORAGE, user)
    userExists = os.path.exists(userPath)

    if not userExists:
        os.makedirs(userPath)

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y-%m-%d_%H-%M-%S")

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


@app.route("/users/<username>/photos", methods=["POST"])
def image_upload(username):
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
