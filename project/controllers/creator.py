# -*- coding: utf-8 -*-
import base64
import io
import os

from io import StringIO
import matplotlib.pyplot as plt
from PIL import Image

from project import app
from flask import render_template, request, redirect, make_response, render_template_string, send_from_directory, \
    Response
from flask_wtf import FlaskForm
from includes.creator import *
from project import pages as pages_session
from project.components import Analysis


class CreatorController(FlaskForm):
    name = "creator"


def add_pages(new_pages):
    for page in new_pages:
        pages_session[page.identifier] = page


def add_page(page):
    pages_session[page.identifier] = page


@app.route('/browse/<identifier>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def browser(identifier):
    page = pages_session[identifier]

    if page.__class__.__name__ == "RedirectPage":
        return redirect(page.redirect, page.status)

    if page.form is not None:
        form = page.form.build_form(request)

        if request.method == page.form.method and form.validate():
            if page.form.action is not None:
                return redirect(page.form.action, code=200)
    else:
        form = {}

    response = make_response(
        render_template(
            'creator/browser.html',
            form=form,
            page=page
        )
    )

    for header in page.headers:
        response.headers.set(header.name, header.value)

    response.status_code = page.status

    return response


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
    pages1.append(RedirectPage("demo-redirect", "/browse/demo"))
    add_pages(pages1)
    links1 = LinkCreator().generate_links_for_page(pages1)

    pages2 = PageCreator().generate_n_pages(5)
    pages2.append(Page("demo-headers", headers={
        Header("Content-Type", "application/json")
    }))
    add_pages(pages2)
    links2 = LinkCreator().generate_links_for_page(pages2)

    action_page = Page("demo-action", links=links1)
    page = Page("demo", form=form, links=links2)

    add_pages([page, action_page])

    return render_template('creator/demo.html', index="demo")


@app.route('/analysis/<tool>')
def analysis(tool):
    width = 1900
    height = 1200
    Analysis.request_method(tool)

    images = []
    for root, dirs, files in os.walk('.'):
        for filename in [os.path.join(root, name) for name in files]:
            # print("FILENAME: " + str(filename))
            if not (filename.endswith('.jpg') and filename.startswith('./%s' % tool)):
                continue
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            if aspect > 1.0*width/height:
                width = min(w, width)
                height = width/aspect
            else:
                height = min(h, height)
                width = height*aspect
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })

    # print("IMAGES: " + str(images))
    return render_template_string('{% extends "creator/analysis.html" %}',
                                  **{'images': images})


@app.route('/analysis')
def select_analysis():
    return render_template('creator/select_analysis.html')
