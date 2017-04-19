# -*- coding: utf-8 -*-
from flask import request, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField

from includes.creator import ParamCreator, LinkCreator, PageCreator, Header
from project import app
from project.components import Settings


class GeneratorController(FlaskForm):
    name = "generator"
    params_num = IntegerField("Params num")
    links_num = IntegerField("Pages num")
    status = IntegerField('status')
    headers = TextAreaField('headers')

    @staticmethod
    def prepare_headers(raw_headers):
        headers = []

        for raw_header in raw_headers.splitlines():
            header = raw_header.replace(": ", ":").split(":")
            headers.append(Header(header[0], header[1]))

        return headers


@app.route('/<test_id>/<page_id>/generator', methods=['GET', 'POST'])
def generator(test_id, page_id):
    settings = Settings.load()

    page = settings.tests[test_id][page_id]

    form = GeneratorController(request.form)
    form.params_num.data = 0
    form.links_num.data = 0
    form.status.data = 200

    if request.method == "POST" and form.validate():
        form = GeneratorController(request.form)

        if form.params_num.data > 0:
            param_creator = ParamCreator()
            param_creator.generate_n_params(form.params_num.data)
            page.params = {**page.params, **param_creator.params}
            
        if form.links_num.data > 0:
            link_creator = LinkCreator()
            page_creator = PageCreator()

            page_creator.generate_n_pages(
                form.links_num.data,
                status=form.status.data,
                headers=GeneratorController.prepare_headers(form.headers.data)
            )

            settings.tests[test_id] = {**settings.tests[test_id], **page_creator.pages}

            link_creator.generate_links_for_page(page_creator.pages)

            page.links += link_creator.links

        settings.save()

        return redirect("/" + test_id + "/pages", 302)

    return render_template('generator/generator.html', page_id=page_id, form=form, test_id=test_id)
