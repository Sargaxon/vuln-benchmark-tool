# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request, redirect, make_response
from flask_wtf import FlaskForm
from includes.creator import *
from project import pages as pages_session


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
