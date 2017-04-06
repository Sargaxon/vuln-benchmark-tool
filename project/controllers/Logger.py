from flask import render_template

from includes.creator import FormCreator
from project import app


@app.route('/creator/log')
def log():
    form = FormCreator("POST", "log-action")

    return render_template('creator/log.html')

