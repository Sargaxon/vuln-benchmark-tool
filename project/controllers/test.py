# -*- coding: utf-8 -*-
from wtforms import StringField
from wtforms.validators import DataRequired

from project import app
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from project.components import Settings


class TestController(FlaskForm):
    name = "test"
    identifier = StringField('identifier', validators=[DataRequired()])


@app.route('/tests')
def list_tests():
    settings = Settings.load()

    tests = settings.tests

    return render_template('test/list.html', tests=tests)


@app.route('/tests/new', methods=['GET', 'POST'])
def new_test():
    settings = Settings.load()

    form = TestController(request.form)

    if request.method == "POST" and form.validate():
        test_id = form.identifier.data

        settings.tests[test_id] = dict()
        settings.save()

        return redirect("/tests", 302)

    return render_template('test/new.html', form=form)


@app.route('/tests/edit/<test_id>', methods=['GET', 'POST'])
def edit_test(test_id):
    settings = Settings.load()

    form = TestController(request.form)
    form.identifier.data = test_id

    if request.method == "POST" and form.validate():
        form = TestController(request.form)

        del settings.tests[test_id]
        test_id = form.identifier.data

        settings.tests[test_id] = dict()
        settings.save()

        return redirect("/tests", 302)

    return render_template('test/edit.html', form=form, test_id=test_id)


@app.route('/tests/delete/<test_id>')
def delete_test(test_id):
    settings = Settings.load()

    del settings.tests[test_id]
    settings.save()

    return redirect("/tests", 302)
