# # -*- coding: utf-8 -*-
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
__version__ = '0.2'

app = Flask('benchmark')
app.config.update(dict(
    DATABASE='postgresql+psycopg2://postgres:postgres@localhost:5432/postgres',
    SECRET_KEY='random',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASK_SETTINGS', silent=True)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = False

toolbar = DebugToolbarExtension(app)
from benchmark.controllers import benchmark
from project.database.Database import session


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
