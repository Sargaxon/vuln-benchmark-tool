from project.models.Request import Request


def request_insert():
    print("REQUEST INSERT")
    data = {
        "datetime": "ab11",
        "tool": "bdf",
        "first_line_format": "cdfd",
        "method": "cfd",
        "scheme": "cdd",
        "host": "cdd",
        "port": "dddc",
        "path": "cdd",
        "http_version": "cdddf",
        "headers": "cdf",
        "content": "cdfd",
        "timestamp_start": "cdfd",
        "timestamp_end": "cfdf"
    }

    request = Request()
    request.load(data)
    request.insert()


def request_update():
    print("REQUEST UPDATE")
    request = Request.find_one(730)
    request.tool = "updated"
    request.update()


def request_delete():
    print("REQUEST DELETE")
    request = Request.find_one(730)
    request.delete()


