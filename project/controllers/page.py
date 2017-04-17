# -*- coding: utf-8 -*-
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired
from os import linesep

from includes.creator import Page, Header
from project import app
from flask import render_template, redirect, request
from flask_wtf import FlaskForm
from project.components import Settings


class PageController(FlaskForm):
    name = "page"
    identifier = StringField('identifier', validators=[DataRequired()])
    status = IntegerField('status', validators=[DataRequired()])
    headers = TextAreaField('headers')

    @staticmethod
    def prepare_headers(raw_headers):
        headers = []

        for raw_header in raw_headers.splitlines():
            header = raw_header.replace(": ", ":").split(":")
            headers.append(Header(header[0], header[1]))

        return headers

    @staticmethod
    def raw_headers(headers):
        raw_headers = ""

        for header in headers:
            raw_headers += header.name + ": " + header.value + linesep

        return raw_headers


@app.route('/<test_id>/pages')
def list_pages(test_id):
    settings = Settings.load()

    pages = settings.tests[test_id]

    return render_template('page/list.html', pages=pages, test_id=test_id)


@app.route('/<test_id>/pages/new', methods=['GET', 'POST'])
def new_page(test_id):
    settings = Settings.load()

    form = PageController(request.form)

    if request.method == "POST" and form.validate():
        page = Page(form.identifier.data, form.status.data, headers=PageController.prepare_headers(form.headers.data))

        settings.tests[test_id][page.identifier] = page
        settings.save()

        return redirect("/" + test_id + "/pages", 302)

    return render_template('page/new.html', form=form, test_id=test_id)


@app.route('/<test_id>/pages/edit/<page_id>', methods=['GET', 'POST'])
def edit_page(test_id, page_id):
    settings = Settings.load()

    page = settings.tests[test_id][page_id]

    form = PageController(request.form)
    form.identifier.data = page.identifier
    form.status.data = page.status
    form.headers.data = PageController.raw_headers(page.headers)

    if request.method == "POST" and form.validate():
        form = PageController(request.form)

        del settings.tests[test_id][page_id]
        page.headers = PageController.prepare_headers(form.headers.data)
        page.status = form.status.data
        page.identifier = form.identifier.data

        settings.tests[test_id][page.identifier] = page
        settings.save()

        return redirect("/" + test_id + "/pages", 302)

    return render_template('page/edit.html', form=form, test_id=test_id)


@app.route('/<test_id>/pages/delete/<page_id>')
def delete_page(test_id, page_id):
    settings = Settings.load()

    del settings.tests[test_id][page_id]
    settings.save()

    return redirect("/" + test_id + "/pages", 302)
