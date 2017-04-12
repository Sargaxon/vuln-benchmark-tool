# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SelectField

from includes.creator import Link
from project import app
from flask import render_template, redirect, request
from project.components import Settings


class LinkController(FlaskForm):
    controller_name = "link"
    page = SelectField("page")

    @staticmethod
    def create_pages_drop_down(pages):
        drop_down = []

        for (identifier, page) in pages.items():
            drop_down.append((identifier, identifier))

        return drop_down


@app.route('/<test_id>/<page_id>/links')
def list_links(test_id, page_id):
    settings = Settings.load()

    links = settings.tests[test_id][page_id].links

    return render_template('link/list.html', links=enumerate(links), test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/links/new', methods=['GET', 'POST'])
def new_link(test_id, page_id):
    settings = Settings.load()

    form = LinkController(request.form)
    form.page.choices = LinkController.create_pages_drop_down(settings.tests[test_id])

    if request.method == "POST" and form.validate():
        link = Link(settings.tests[test_id][form.page.data])

        settings.tests[test_id][page_id].links.append(link)
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/links", 302)

    return render_template('link/new.html', form=form, test_id=test_id, page_id=page_id)


@app.route('/<test_id>/<page_id>/links/edit/<link_id>', methods=['GET', 'POST'])
def edit_link(test_id, page_id, link_id):
    settings = Settings.load()

    link = settings.tests[test_id][page_id].links[int(link_id)]

    form = LinkController(request.form)
    form.page.choices = LinkController.create_pages_drop_down(settings.tests[test_id])
    form.page.data = link.page.identifier

    if request.method == "POST" and form.validate():
        form.process(request.form)

        link = Link(settings.tests[test_id][form.page.data])

        settings.tests[test_id][page_id].links[int(link_id)] = link
        settings.save()

        return redirect("/" + test_id + "/" + page_id + "/links", 302)

    return render_template('link/edit.html', form=form, test_id=test_id, page_id=page_id, link_id=link_id)


@app.route('/<test_id>/<page_id>/links/delete/<link_id>')
def delete_link(test_id, page_id, link_id):
    settings = Settings.load()

    settings.tests[test_id][page_id].links.pop(int(link_id))
    settings.save()

    return redirect("/" + test_id + "/" + page_id + "/links", 302)
