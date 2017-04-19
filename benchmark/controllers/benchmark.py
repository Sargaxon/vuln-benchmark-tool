# -*- coding: utf-8 -*-
from benchmark import app, PORT
from flask import render_template, redirect, make_response
from flask_wtf import FlaskForm
from project.components import Settings
import datetime
from flask import request
from project.models.Request import Request
from project.models.RequestHeader import RequestHeader


class BenchmarkController(FlaskForm):
    name = "benchmark"


@app.route('/')
def start():
    settings = Settings.load()

    redirect("/" + settings.index_page, 302)


@app.route('/<identifier>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def browser(identifier):
    settings = Settings.load()
    page = settings.session[identifier]

    if page.__class__.__name__ == "RedirectPage":
        return redirect(page.redirect, page.status)

    if page.form is not None:
        page.form.build_form()
        form = page.form.process_form(request)
    else:
        form = {}

    response = make_response(
        render_template(
            'benchmark/browser.html',
            form=form,
            page=page
        )
    )

    for header in page.headers:
        response.headers.set(header.name, header.value)

    response.status_code = page.status

    return response

tool_name = Settings.load().tool
app_name = "vuln-benchmark-tool"

request_header_fields = [
    'Accept', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language', 'Accept-Datetime',
    'Connection', 'Authorization', 'Cache-Control', 'Cookie', 'Content-Length',
    'Content-MD5', 'Content-Type', 'Date', 'Expect', 'Forwarded', 'From', 'Host',
    'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range', 'If-Unmodified-Since',
    'Max-Forwards', 'Origin', 'Pragma', 'Proxy-Authorization', 'Proxy-Connection', 'Range',
    'Referer', 'TE', 'User-Agent', 'Upgrade', 'Via', 'Warning']


@app.before_request
def log_request_info():
    data = {
        "datetime": datetime.datetime.now(),
        "tool": tool_name,
        "first_line_format": "null",
        "method": request.method,
        "scheme": "null",
        "host": 'localhost',
        "port": PORT,
        "path": request.path,
        "http_version": "HTTP/1.1",
        "headers": "null",
        "content": request.data,
        "timestamp_start": str(datetime.datetime.now()),
        "timestamp_end": "null"
    }
    req = Request(**data)
    req.insert()

    """HEADERS"""
    request_header_data = {}

    for i in range(0, len(request_header_fields)):
        if request_header_fields[i] not in request.headers:
            continue
            # request.headers[request_header_fields[i]] = "null"

        request_header_data[request_header_fields[i].lower().replace("-", "_")] = \
            str(request.headers[request_header_fields[i]])

    header = RequestHeader(**request_header_data)
    header.id_request = req.id
    header.insert()
