from collections import OrderedDict

from flask import render_template, Markup, flash, abort

from benchmark.controllers import benchmark
from includes.creator import FormCreator
from project import app, PER_PAGE
from project.components import Pagination
from project.models.RequestHeader import RequestHeader
from project.models.Request import Request


def print_log(requests):
    for r in requests:
        message = Markup("<p><b>Request [{0}]:"
                         "<br>Id:</b> {1}"
                         "<br><b>Method:</b> {2}"
                         "<br><b>Host:</b> {3}"
                         "<br><b>Path:</b> {4}"
                         "<br><a class='secondary-content' href='/creator/log/view={1}'><i class='small material-icons'>pageview</i></a>"
                         "<a class='secondary-content' href='/creator/log/delete={1}'><i class='small material-icons'>delete</i></a></p><br /><br />".format(r.datetime, r.id, r.method, r.host, r.path))
        flash(message)


def print_view(req_id):
    r = Request.find_one(req_id)

    message = Markup("<p><b>Request [{0}]:"
                     "<br>Id:</b> {1}"
                     "<br><b>Tool:</b> {2}"
                     "<br><b>First line format:</b> {3}"
                     "<br><b>Method:</b> {4}"
                     "<br><b>Scheme:</b> {5}"
                     "<br><b>Host:</b> {6}"
                     "<br><b>Port:</b> {7}"
                     "<br><b>Path:</b> {8}"
                     "<br><b>Http version:</b> {9}"
                     "<br><b>Content:</b> {10}"
                     "<br><b>Timestamp start:</b> {11}"
                     "<br><b>Timestamp end:</b> {12}"
                     "</p>".format(r.datetime, r.id, r.tool, r.first_line_format, r.method, r.scheme, r.host, r.port, r.path, r.http_version, r.content, r.timestamp_start, r.timestamp_end))
    flash(message)

    rh = RequestHeader.find_one(req_id)
    message = "<p><b>Request Headers:</b>"
    for field in benchmark.request_header_fields:
        if getattr(rh, field.lower(), 0):
            message += "<br><b>{0}:</b> {1}".format(field, getattr(rh, field.lower()))
            # print("<br><b>{0}:</b> {1}".format(field, getattr(rh, field.lower())))
        else:
            message += "<br><b>{0}:</b> null".format(field)
    message += "</p>"
    flash(message)

    message = "<p><a href='/creator/log'>Back</a>   " \
              "<a href='/creator/log/delete={0}'>Delete</a></p>".format(req_id)
    flash(message)


@app.route('/creator/log', defaults={'page': 1})
@app.route('/creator/log/<int:page>')
def log(page):
    requests = Request.query.offset(page * PER_PAGE).limit(PER_PAGE).all()

    count = Request.query.count()

    if not requests and page != 1:
        abort(404)

    pagination = Pagination(page, PER_PAGE, count)

    print_log(requests)

    return render_template('creator/log.html', pagination=pagination)


@app.route('/creator/log/view=<int:req_id>')
def view(req_id):
    form = FormCreator("POST", "log-action")

    print_view(req_id)
    return render_template('creator/view.html')


@app.route('/creator/log/delete=<int:req_id>')
def delete(req_id):
    form = FormCreator("POST", "log-action")

    RequestHeader.delete(req_id)
    Request.delete(req_id)
    message = "<p>Request with id {0} deleted!" \
              "<br><a href='/creator/log'>Back</a></p>".format(req_id)
    flash(message)
    return render_template('creator/delete.html')


@app.route('/creator/log/edit=<int:req_id>')
def edit(req_id):
    form = FormCreator("POST", "log-action")
    form.add_text_field("Datetime")
    form.add_text_field("Tool")
    form.add_text_field("First line format")
    form.add_text_field("Method")
    form.add_text_field("Scheme")
    form.add_text_field("Host")
    form.add_text_field("Port")
    form.add_text_field("Path")
    form.add_text_field("Http version")
    form.add_text_field("Headers")
    form.add_text_field("Content")
    form.add_text_field("Timestamp start")
    form.add_text_field("Timestamp end")

    return render_template('creator/edit.html')
