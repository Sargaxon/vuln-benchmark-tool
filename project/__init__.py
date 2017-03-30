# # -*- coding: utf-8 -*-
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
__version__ = '0.2'

app = Flask('project')
app.config.update(dict(
    DATABASE='postgresql+psycopg2://postgres:postgres@localhost:5432/postgres',
    SECRET_KEY='random',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.debug = True

pages = dict()

toolbar = DebugToolbarExtension(app)
from project.controllers import *
from project.models import *
from project.database.Database import session


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
