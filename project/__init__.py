# # -*- coding: utf-8 -*-
from flask import Flask, url_for, request
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
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True

tools = [
    ("unknown", "Unknown"),
    ("zaproxy", "OWASP ZAP"),
    ("w3af", "W3af"),
    ("tool_n", "Tool N"),
    ("skipfish", "Skipfish"),
    ("arachi", "Arachi Scanner"),
    ("tool_b", "Tool B")
]

PER_PAGE = 25

toolbar = DebugToolbarExtension(app)
from project.controllers import *
from project.models import *
from project.database.Database import session


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page
