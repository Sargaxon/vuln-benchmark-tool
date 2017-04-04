# -*- coding: utf-8 -*-
import os

from wtforms import StringField, IntegerField
from wtforms.form import BaseForm

from project import app
from flask import render_template, request, redirect, session, Markup, flash
from flask_wtf import FlaskForm
from includes.creator import *
from project import pages as pages_session
from subprocess import call

class CreatorController(FlaskForm):
    name = "creator"


def add_pages(new_pages):
    for page in new_pages:
        pages_session[page.identifier] = page


def add_page(page):
    pages_session[page.identifier] = page


@app.route('/creator/new')
def new():
    pages_session = dict()

    return render_template('creator/new.html')


@app.route('/browse/<identifier>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def browser(identifier):
    page = pages_session[identifier]

    if page.form is not None:
        form = page.form.build_form(request)

        if request.method == page.form.method and form.validate():
            if page.form.action is not None:
                return redirect(page.form.action, code=200)
    else:
        form = {}

    return render_template(
        'creator/browser.html',
        form=form,
        page=page
    )


@app.route('/creator/demo')
def demo():
    pages_session = dict()

    form = FormCreator("POST", "demo-action")
    form.add_text_field("text-field1")
    form.add_number_field("number-field1", True)
    form.add_text_field("text-field2", True)
    form.add_checkbox_field("checkbox-field1")
    form.add_select_field(
        "select-field1",
        [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )
#   form.add_radio_field("radio-field1") needs further testing

    pages1 = PageCreator().generate_n_pages(5, 0)
    add_pages(pages1)
    links1 = LinkCreator().generate_links_for_pages(pages1)

    pages2 = PageCreator().generate_n_pages(5)
    add_pages(pages2)
    links2 = LinkCreator().generate_links_for_pages(pages2, 0)

    action_page = Page("demo-action", links=links1)
    page = Page("demo", form=form, links=links2)

    add_pages([page, action_page])

    return render_template('creator/demo.html', index="demo")


@app.route('/creator/log')
def log():
    form = FormCreator("POST", "log-action")

    # if request.method == 'POST':
    #     if request.form['submit'] == 'started':
    #         message = Markup("<p>Started</p>")
    #         flash(message)
    #         for i in range(0, 30):
    #             message = Markup("<p>Sir, we have transmitted our %i. message</p>" % i)
    #             flash(message)
    #     elif request.form['submit'] == 'stopped':
    #         message = Markup("<p>Stopped</p>")
    #         flash(message)
    #
    # elif request.method == 'GET':
    call(["mitmdump", "-s", "%s/Logger.py" % os.path.dirname(os.path.realpath(__file__)), "-p", "9999"])
    return render_template('creator/log.html')

