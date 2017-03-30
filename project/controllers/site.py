# -*- coding: utf-8 -*-
from project import app
from flask import render_template


class SiteController:
    def __init__(self):
        self.identifier = "site"


@app.route('/')
def start():
    return render_template('site/index.html')


@app.route('/404')
def not_found():
    return render_template('site/404.html')
