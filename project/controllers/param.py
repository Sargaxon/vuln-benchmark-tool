# -*- coding: utf-8 -*-
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

from includes.creator import Page, Param
from project import app
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from project.components import Settings


class ParamController(FlaskForm):
    controller_name = "param"
    name = StringField('name', validators=[DataRequired()])
    value = IntegerField('value', validators=[DataRequired()])


@app.route('/<test_id>/<page_id>/params')
def list_params(test_id, page_id):
    settings = Settings.load()

    params = settings.tests[test_id][page_id].params

    return render_template('param/list.html', params=params, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/params/new', methods=['GET', 'POST'])
def new_param(test_id, page_id):
    settings = Settings.load()

    form = ParamController(request.form)

    if request.method == "POST" and form.validate():
        param = Param(form.name.data, form.value.data)

        settings.tests[test_id][page_id].params[param.name] = param
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/params", 302)

    return render_template('param/new.html', form=form, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/params/edit/<param_id>', methods=['GET', 'POST'])
def edit_param(test_id, page_id, param_id):
    settings = Settings.load()

    param = settings.tests[test_id][page_id].params[param_id]

    form = ParamController(request.form)
    form.name.data = param.name
    form.value.data = param.value

    if request.method == "POST" and form.validate():
        form = ParamController(request.form)

        del settings.tests[test_id][page_id].params[param_id]
        param = Param(form.name.data, form.value.data)

        settings.tests[test_id][page_id].params[param.name] = param
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/params", 302)

    return render_template('param/edit.html', form=form, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/params/delete/<param_id>')
def delete_param(test_id, page_id, param_id):
    settings = Settings.load()

    del settings.tests[test_id][page_id].params[param_id]
    settings.save()

    return redirect("/" + test_id + "/" + page_id + "/params", 302)
