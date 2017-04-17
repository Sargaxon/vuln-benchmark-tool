# -*- coding: utf-8 -*-
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import DataRequired

from project import app
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from project.components import Settings


class FieldController(FlaskForm):
    controller_name = "field"
    name = StringField('name', validators=[DataRequired()])
    required = BooleanField('required')
    type = SelectField('type', choices=[
        ("text", "Text"), ("number", "Number"), ("select", "Select"), ("checkbox", "Checkbox"), ("radio", "Radio")
    ])


class ChoiceController(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    value = StringField('value', validators=[DataRequired()])


def select(case, form, form_creator):
    {
        "text": form_creator.add_text_field,
        "number": form_creator.add_number_field,
        "select": form_creator.add_select_field,
        "checkbox": form_creator.add_checkbox_field,
        "radio": form_creator.add_radio_field
    }[case](form.name.data, form.required.data)

    return form_creator


@app.route('/<test_id>/<page_id>/form/fields/new', methods=['GET', 'POST'])
def new_field(test_id, page_id):
    settings = Settings.load()

    form_creator = settings.tests[test_id][page_id].form

    form = FieldController(request.form)

    if request.method == "POST" and form.validate():
        form_creator = select(form.type.data, form, form_creator)

        settings.tests[test_id][page_id].form = form_creator
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/form", 302)

    return render_template('field/new.html', form=form, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/form/fields/<field_id>/choices')
def list_choices(test_id, page_id, field_id):
    settings = Settings.load()

    field = settings.tests[test_id][page_id].form.elements[field_id]

    if field.element_type != "SelectField":
        return redirect("/" + test_id + "/" + page_id + "/form", 302)

    return render_template('field/choices/list.html',
                           field_id=field_id,
                           choices=field.choices,
                           test_id=test_id,
                           page_id=page_id
                           )


@app.route('/<test_id>/<page_id>/form/fields/<field_id>/choices/new', methods=['GET', 'POST'])
def new_choice(test_id, page_id, field_id):
    settings = Settings.load()

    field = settings.tests[test_id][page_id].form.elements[field_id]
    form_creator = settings.tests[test_id][page_id].form

    if field.element_type != "SelectField":
        return redirect("/" + test_id + "/" + page_id + "/form", 302)

    form = ChoiceController(request.form)

    if request.method == "POST" and form.validate():
        form = ChoiceController(request.form)

        field.choices.append((form.name.data, form.value.data))
        form_creator.add_select_field(field_id, required=False, options=field.choices)

        settings.tests[test_id][page_id].form = form_creator
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/form/fields/" + field_id + "/choices", 302)

    return render_template('field/choices/new.html',
                           field_id=field_id,
                           test_id=test_id,
                           page_id=page_id,
                           form=form
                           )


@app.route('/<test_id>/<page_id>/form/fields/<field_id>/choices/delete/<choice_id>')
def delete_choice(test_id, page_id, field_id, choice_id):
    settings = Settings.load()

    field = settings.tests[test_id][page_id].form.elements[field_id]

    if field.element_type != "SelectField":
        return redirect("/" + test_id + "/" + page_id + "/form", 302)

    del settings.tests[test_id][page_id].form.elements[field_id].choices[choice_id]
    settings.save()

    return redirect("/" + test_id + "/" + page_id + "/form/fields/" + field_id + "/choices", 302)


@app.route('/<test_id>/<page_id>/form/fields/delete/<field_id>')
def delete_field(test_id, page_id, field_id):
    settings = Settings.load()

    del settings.tests[test_id][page_id].form.elements[field_id]
    settings.save()

    return redirect("/" + test_id + "/" + page_id + "/form", 302)
