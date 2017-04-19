import datetime

from werkzeug.datastructures import TypeConversionDict

from project import app
from flask import request, Markup, flash

from project.models.Request import Request
from project.models.RequestHeader import RequestHeader

tool_name = "w3af"
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
    if request.path.startswith('/browse'):
        data = {
            "datetime": datetime.datetime.now(),
            "tool": tool_name,
            "first_line_format": "null",
            "method": request.method,
            "scheme": "null",
            "host": 'localhost',
            "port": '8080',
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
