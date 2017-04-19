# -*- coding: utf-8 -*-
from project import app
from flask import send_file


class ImageController:
    def __init__(self):
        self.identifier = "image"


@app.route('/images/<file_name>')
def image(file_name):
    return send_file('../' + file_name, mimetype="image/jpeg")

