import datetime
import psycopg2

conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres'")
cur = conn.cursor()

tool = "zaproxy"
app = "wordpress"

request_header_fields = [
    'Accept', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language', 'Accept-Datetime',
    'Connection', 'Authorization', 'Cache-Control', 'Cookie', 'Content-Length',
    'Content-MD5', 'Content-Type', 'Date', 'Expect', 'Forwarded', 'From', 'Host',
    'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range', 'If-Unmodified-Since',
    'Max-Forwards', 'Origin', 'Pragma', 'Proxy-Authorization', 'Proxy-Connection', 'Range',
    'Referer', 'TE', 'User-Agent', 'Upgrade', 'Via', 'Warning']

response_header_fields = [
    'Access-Control-Allow-Origin', 'Accept-Patch', 'Accept-Ranges', 'Age', 'Allow',
    'Alt-Svc', 'Cache-Control', 'Connection', 'Content-Disposition', 'Content-Encoding',
    'Content-Language', 'Content-Length', 'Content-Location', 'Content-MD5', 'Content-Range',
    'Content-Type', 'Date', 'ETag', 'Expires', 'Last-Modified', 'Link', 'Location',
    'P3P', 'Pragma', 'Proxy-Authenticate', 'Public-Key-Pins', 'Refresh', 'Retry-After',
    'Server', 'Set-Cookie', 'Status', 'Strict-Transport-Security', 'Trailer',
    'Transfer-Encoding', 'TSV', 'Upgrade', 'Vary', 'Via', 'Warning', 'WWW-Authenticate',
    'X-Frame-Options']


def request(flow):
    print("REQUEST POCETAK")
    log_httpflow = open("log_http_flow.txt", "a")
    log_data = open("log_data.txt", "a")
    req = "\n[HTTPRequest %s]" % str(datetime.datetime.now()) + "\n" + \
          "TOOL: %s" % tool + "\n" + \
          "FIRST_LINE_FORMAT: %s" % flow.request.first_line_format + "\n" + \
          "METHOD: %s" % flow.request.method + "\n" + \
          "SCHEME: %s" % flow.request.scheme + "\n" + \
          "HOST: %s" % flow.request.host + "\n" + \
          "PORT: %s" % flow.request.port + "\n" + \
          "PATH: %s" % flow.request.path + "\n" + \
          "HTTP_VERSION: %s" % flow.request.http_version + "\n" + \
          "HEADERS: %s" % flow.request.headers + "\n" + \
          "CONTENT: %s" % str(flow.request.content) + "\n" + \
          "TIMESTAMP_START: %s" % flow.request.timestamp_start + "\n" + \
          "TIMESTAMP_END: %s" % flow.request.timestamp_end + "\n"
    log_httpflow.write("REQUEST [%s]: " % str(datetime.datetime.now()) + str(flow) + "\n")
    log_data.write(req)
    log_httpflow.close()
    log_data.close()

    data = {
        "HTTPRequest": str(datetime.datetime.now()),
        "TOOL": tool,
        "FIRST_LINE_FORMAT": flow.request.first_line_format,
        "METHOD": flow.request.method,
        "SCHEME": flow.request.scheme,
        "HOST": flow.request.host,
        "PORT": flow.request.port,
        "PATH": flow.request.path,
        "HTTP_VERSION": flow.request.http_version,
        "HEADERS": str(flow.request.headers),
        "CONTENT": str(flow.request.content),
        "TIMESTAMP_START": str(flow.request.timestamp_start),
        "TIMESTAMP_END": str(flow.request.timestamp_end)
    }

    try:
        cur.execute("INSERT INTO requests "
                    "(datetime, "
                    "tool, "
                    "first_line_format, "
                    "method,"
                    "scheme, "
                    "host, "
                    "port, "
                    "path, "
                    "http_version, "
                    "headers, "
                    "content, "
                    "timestamp_start, "
                    "timestamp_end) "
                    "VALUES ("
                    "%(HTTPRequest)s, "
                    "%(TOOL)s, "
                    "%(FIRST_LINE_FORMAT)s, "
                    "%(METHOD)s, "
                    "%(SCHEME)s, "
                    "%(HOST)s, "
                    "%(PORT)s, "
                    "%(PATH)s, "
                    "%(HTTP_VERSION)s, "
                    "%(HEADERS)s, "
                    "%(CONTENT)s, "
                    "%(TIMESTAMP_START)s, "
                    "%(TIMESTAMP_END)s);", data)
    except Exception as e:
        print(e)
    conn.commit()


    # ----- REQUEST_HEADERS -----

    # log_requests_headers = open("log_requests_headers.txt", "a")
    request_header_data = {}

    print("REQUEST ULAZ U PETLJU")

    for i in range(0, len(request_header_fields)):
        if request_header_fields[i] not in flow.request.headers:
            flow.request.headers[request_header_fields[i]] = ""

        request_header_data[request_header_fields[i].upper().replace("-", "_")] = \
            str(flow.request.headers[request_header_fields[i]])

        # for key, value in request_header_data.items():
        #     log_requests_headers.write('%s:%s\n' % (key, value))

    # log_requests_headers.close()

    print("REQUEST ULAZ U UPIT")
    try:
        cur.execute("INSERT INTO requests_headers "
                    "(accept, "
                    "accept_charset, "
                    "accept_encoding, "
                    "accept_language,"
                    "accept_datetime, "
                    "connection, "
                    "h_authorization, "
                    "cache_control, "
                    "cookie, "
                    "content_length, "
                    "content_md5, "
                    "content_type, "
                    "date, "
                    "expect, "
                    "forwarded, "
                    "h_from, "
                    "host, "
                    "if_match, "
                    "if_modified_since, "
                    "if_none_match, "
                    "if_range, "
                    "if_unmodified_since, "
                    "max_forwards, "
                    "origin, "
                    "pragma, "
                    "proxy_authorization, "
                    "proxy_connection, "
                    "range, "
                    "referer, "
                    "te, "
                    "user_agent, "
                    "upgrade, "
                    "via, "
                    "warning) "
                    "VALUES ("
                    "%(ACCEPT)s, "
                    "%(ACCEPT_CHARSET)s, "
                    "%(ACCEPT_ENCODING)s, "
                    "%(ACCEPT_LANGUAGE)s, "
                    "%(ACCEPT_DATETIME)s, "
                    "%(CONNECTION)s, "
                    "%(AUTHORIZATION)s, "
                    "%(CACHE_CONTROL)s, "
                    "%(COOKIE)s, "
                    "%(CONTENT_LENGTH)s, "
                    "%(CONTENT_MD5)s, "
                    "%(CONTENT_TYPE)s, "
                    "%(DATE)s, "
                    "%(EXPECT)s, "
                    "%(FORWARDED)s, "
                    "%(FROM)s, "
                    "%(HOST)s, "
                    "%(IF_MATCH)s, "
                    "%(IF_MODIFIED_SINCE)s, "
                    "%(IF_NONE_MATCH)s, "
                    "%(IF_RANGE)s, "
                    "%(IF_UNMODIFIED_SINCE)s, "
                    "%(MAX_FORWARDS)s, "
                    "%(ORIGIN)s, "
                    "%(PRAGMA)s, "
                    "%(PROXY_AUTHORIZATION)s, "
                    "%(PROXY_CONNECTION)s, "
                    "%(RANGE)s, "
                    "%(REFERER)s, "
                    "%(TE)s, "
                    "%(USER_AGENT)s, "
                    "%(UPGRADE)s, "
                    "%(VIA)s, "
                    "%(WARNING)s);", request_header_data)
    except Exception as e:
        print(e)

    conn.commit()
    print("REQUEST UPIT COMMITAN")

def response(flow):
    print("RESPONSE POCETAK")
    log = open("log_data.txt", "a")
    resp = "\n[HTTPResponse %s]" % str(datetime.datetime.now()) + "\n" + \
           "APP: %s" % app + "\n" + \
           "HTTP_VERSION: %s" % flow.response.http_version + "\n" + \
           "STATUS_CODE: %s" % flow.response.status_code + "\n" + \
           "REASON: %s" % flow.response.reason + "\n" + \
           "HEADERS: %s" % str(flow.response.headers) + "\n" + \
           "CONTENT: %s" % flow.response.content + "\n" + \
           "TIMESTAMP_START: %s" % flow.response.timestamp_start + "\n" + \
           "TIMESTAMP_END: %s" % flow.response.timestamp_end + "\n"
    log.write(resp)
    log.close()

    data = {
        "HTTPResponse": str(datetime.datetime.now()),
        "APP": app,
        "HTTP_VERSION": flow.response.http_version,
        "STATUS_CODE": flow.response.status_code,
        "REASON": flow.response.reason,
        "HEADERS": str(flow.response.headers),
        "CONTENT": flow.response.content,
        "TIMESTAMP_START": str(flow.response.timestamp_start),
        "TIMESTAMP_END": str(flow.response.timestamp_end)
    }

    try:
        cur.execute("INSERT INTO responses "
                    "(datetime, "
                    "app, "
                    "http_version, "
                    "status_code, "
                    "reason, "
                    "headers, "
                    "content, "
                    "timestamp_start, "
                    "timestamp_end)"
                    "VALUES ("
                    "%(HTTPResponse)s, "
                    "%(APP)s, "
                    "%(HTTP_VERSION)s, "
                    "%(STATUS_CODE)s, "
                    "%(REASON)s, "
                    "%(HEADERS)s, "
                    "%(CONTENT)s,"
                    "%(TIMESTAMP_START)s, "
                    "%(TIMESTAMP_END)s);", data)
    except Exception as e:
        print(e)

    conn.commit()

    # ----- RESPONSE_HEADERS -----

    # log_response_headers = open("log_response_headers.txt", "a")
    response_header_data = {}

    print("RESPONSE ULAZ U PETLJU")
    for i in range(0, len(response_header_fields)):
        if response_header_fields[i] not in flow.response.headers:
            flow.response.headers[response_header_fields[i]] = ""
        # print("HEADER POLJE: " + str(i) + ") " + str(response_header_fields[i]))

        response_header_data[response_header_fields[i].upper().replace("-", "_")] = \
            str(flow.response.headers[response_header_fields[i]])

        print("HEADER POLJE: " + str(i) + ") " + str(response_header_fields[i]) + " = " +
              str(flow.response.headers[response_header_fields[i]]))

        # for key, value in response_header_data.items():
        #     log_response_headers.write('%s:%s\n' % (key, value))

    # log_response_headers.close()

    try:
        cur.execute("INSERT INTO responses_headers "
                    "(access_control_allow_origin, "
                    "accept_patch, "
                    "accept_ranges, "
                    "age,"
                    "allow, "
                    "alt_svc, "
                    "cache_control, "
                    "connection, "
                    "content_disposition, "
                    "content_encoding, "
                    "content_language, "
                    "content_length, "
                    "content_location, "
                    "content_md5, "
                    "content_range, "
                    "content_type, "
                    "date, "
                    "etag, "
                    "expires, "
                    "last_modified, "
                    "link, "
                    "location, "
                    "p3p, "
                    "pragma, "
                    "proxy_authenticate, "
                    "public_key_pins, "
                    "refresh, "
                    "retry_after, "
                    "server, "
                    "set_cookie, "
                    "status, "
                    "strict_transport_security, "
                    "trailer, "
                    "transfer_encoding, "
                    "tsv, "
                    "upgrade, "
                    "vary, "
                    "via, "
                    "warning, "
                    "www_authenticate, "
                    "x_frame_options) "
                    "VALUES ("
                    "%(ACCESS_CONTROL_ALLOW_ORIGIN)s, "
                    "%(ACCEPT_PATCH)s, "
                    "%(ACCEPT_RANGES)s, "
                    "%(AGE)s, "
                    "%(ALLOW)s, "
                    "%(ALT_SVC)s, "
                    "%(CACHE_CONTROL)s, "
                    "%(CONNECTION)s, "
                    "%(CONTENT_DISPOSITION)s, "
                    "%(CONTENT_ENCODING)s, "
                    "%(CONTENT_LANGUAGE)s, "
                    "%(CONTENT_LENGTH)s, "
                    "%(CONTENT_LOCATION)s, "
                    "%(CONTENT_MD5)s, "
                    "%(CONTENT_RANGE)s, "
                    "%(CONTENT_TYPE)s, "
                    "%(DATE)s, "
                    "%(ETAG)s, "
                    "%(EXPIRES)s, "
                    "%(LAST_MODIFIED)s, "
                    "%(LINK)s, "
                    "%(LOCATION)s, "
                    "%(P3P)s, "
                    "%(PRAGMA)s, "
                    "%(PROXY_AUTHENTICATE)s, "
                    "%(PUBLIC_KEY_PINS)s, "
                    "%(REFRESH)s, "
                    "%(RETRY_AFTER)s, "
                    "%(SERVER)s, "
                    "%(SET_COOKIE)s, "
                    "%(STATUS)s, "
                    "%(STRICT_TRANSPORT_SECURITY)s, "
                    "%(TRAILER)s, "
                    "%(TRANSFER_ENCODING)s, "
                    "%(TSV)s, "
                    "%(UPGRADE)s, "
                    "%(VARY)s, "
                    "%(VIA)s, "
                    "%(WARNING)s, "
                    "%(WWW_AUTHENTICATE)s, "
                    "%(X_FRAME_OPTIONS)s);", response_header_data)
    except Exception as e:
        print(e)
    conn.commit()


def error(flow):
    log_httpflow = open("log_http_flow.txt", "a")
    log_httpflow.write("ERROR [%s]: " % str(datetime.datetime.now()) + str(flow) + "\n")