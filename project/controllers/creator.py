# -*- coding: utf-8 -*-
import os

from wtforms import SelectField
from wtforms.validators import DataRequired

from includes.creator import FormCreator, LinkCreator, PageCreator, RedirectPage, Header, Page
from project import tools
from PIL import Image

from project import app
from flask import render_template, request, redirect, render_template_string
from flask_wtf import FlaskForm
from project.components import Analysis, Settings
from benchmark import PORT


class CreatorController(FlaskForm):
    name = "creator"


class RunController(FlaskForm):
    index = SelectField("Index", validators=[DataRequired()])
    tool = SelectField("Tool", validators=[DataRequired()], choices=tools)

    @staticmethod
    def create_pages_drop_down(pages):
        drop_down = []

        for (identifier, page) in pages.items():
            drop_down.append((identifier, identifier))

        return drop_down


def add_pages(new_pages):
    settings = Settings.load()

    for (identifier, page) in new_pages.items():
        if page.form:
            page.form.build_form()

        settings.session[page.identifier] = page

    settings.save()


def add_page(page):
    settings = Settings.load()
    settings.session[page.identifier] = page
    settings.save()


@app.route('/creator/run/<test_id>', methods=['GET', 'POST'])
def run_test(test_id):
    settings = Settings.load()
    settings.session = dict()
    settings.save()

    if len(settings.tests[test_id]) == 0:
        return redirect("/tests", 302)

    add_pages(settings.tests[test_id])

    form = RunController(request.form)
    form.index.choices = RunController.create_pages_drop_down(settings.tests[test_id])

    if request.method == "POST" and form.validate():
        settings = Settings.load()
        form = RunController(request.form)

        settings.tool = form.tool.data
        settings.index_page = form.index.data
        settings.save()

        return redirect("http://localhost:" + str(PORT) + "/" + form.index.data, 302)

    return render_template("creator/run.html", form=form, test_id=test_id)


@app.route('/creator/demo', methods=['GET', 'POST'])
def demo():
    form = RunController(request.form)
    form.index.choices = [("demo", "demo")]

    demo_form = FormCreator("POST", "demo-action")
    demo_form.add_text_field("text-field1")
    demo_form.add_number_field("number-field1", True)
    demo_form.add_text_field("text-field2", True)
    demo_form.add_checkbox_field("checkbox-field1")
    demo_form.add_select_field(
        "select-field1",
        options=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )

#   form.add_radio_field("radio-field1") needs further testing

    pages1 = PageCreator().generate_n_pages(5, 0)
    pages1["demo-redirect"] = RedirectPage("demo-redirect", "/demo")
    add_pages(pages1)
    links1 = LinkCreator().generate_links_for_page(pages1)

    pages2 = PageCreator().generate_n_pages(5)
    pages2["demo-headers"] = Page("demo-headers", headers={
        Header("Content-Type", "application/json")
    })
    add_pages(pages2)
    links2 = LinkCreator().generate_links_for_page(pages2)

    action_page = Page("demo-action", links=links1)
    page = Page("demo", form=demo_form, links=links2)

    add_pages({page.identifier: page, action_page.identifier: action_page})

    if request.method == "POST" and form.validate():
        settings = Settings.load()
        form = RunController(request.form)

        settings.tool = form.tool.data
        settings.index_page = "demo"
        settings.save()

        return redirect("http://localhost:" + str(PORT) + "/" + form.index.data, 302)

    return render_template('creator/demo.html', index="demo", form=form)


@app.route('/analysis/<tool>')
def analysis(tool):
    width = 1000
    height = 800
    if tool == 'all':
        Analysis.request_comparison()
    elif tool == 'sctr':
        Analysis.scatterplot()
    elif tool == 'testcases':
        Analysis.test_case_comparison()
    else:
        Analysis.request_method(tool)

    images = []
    for root, dirs, files in os.walk('./images'):
        for filename in [os.path.join(root, name) for name in files]:
            # print("FILENAME: " + str(filename))
            if not (filename.endswith('.png') and filename.startswith('./images/%s' % tool)):
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
    return render_template('creator/select_analysis.html', tools=tools)
