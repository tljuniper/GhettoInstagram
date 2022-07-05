#!/usr/bin/env python3

# to execute run `FLASK_APP=main.py FLASK_ENV=DEBUG flask run`

from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)


@app.route("/users/<username>/photos", methods=["POST"])
def image_upload(username):
    print(username)
    data = request.form
    return Response(status=200)


@app.route("/feed", methods=["GET"])
def feed():
    user = request.args.get("users")
    return Response(status=200)


def main():
    print("hello world")


if __name__ == "__main__":
    main()
