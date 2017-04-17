# -*- coding: utf-8 -*-
from wtforms import SelectField

from includes.creator import FormCreator
from project import app
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from project.components import Settings


class FormController(FlaskForm):
    controller_name = "form"
    method = SelectField("method", choices=[("POST", "POST"), ("GET", "GET")])
    page = SelectField("page")

    @staticmethod
    def create_pages_drop_down(pages):
        drop_down = []

        for (identifier, page) in pages.items():
            drop_down.append((identifier, identifier))

        return drop_down


@app.route('/<test_id>/<page_id>/form')
def view_form(test_id, page_id):
    settings = Settings.load()

    form_creator = settings.tests[test_id][page_id].form

    if not form_creator:
        return redirect("/" + test_id + "/" + page_id + "/form/new", 302)

    return render_template('form/form.html',
                           form_creator=form_creator,
                           test_id=test_id,
                           page_id=page_id
                           )


@app.route('/<test_id>/<page_id>/form/new', methods=['GET', 'POST'])
def new_form(test_id, page_id):
    settings = Settings.load()

    form = FormController(request.form)
    form.page.choices = FormController.create_pages_drop_down(settings.tests[test_id])

    if request.method == "POST" and form.validate():
        settings.tests[test_id][page_id].form = FormCreator(form.method.data, form.page.data)
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/form", 302)

    return render_template('form/new.html', form=form, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/form/delete/')
def delete_form(test_id, page_id, form_id):
    settings = Settings.load()

    del settings.tests[test_id][page_id].forms[form_id]
    settings.save()

    return redirect("/" + test_id + "/" + page_id + "/forms", 302)
