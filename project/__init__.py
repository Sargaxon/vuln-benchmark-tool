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

toolbar = DebugToolbarExtension(app)
from project.controllers import *

from project.models import *
from project.database.Database import session, db_create


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
db_create()

#crud test
# from project.tests.crud_model_tests import *
# request_insert()
# request_update()
# request_delete()
# request_query()

