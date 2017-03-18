from project.database.Database import session, db_create, engine
from project.models.Requests import Requests


def request_insert():
    print("REQUEST INSERT")
    data = {
        "datetime": "ab",
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
    session.add(Requests(**data))
    session.commit()


def request_update():
    print("REQUEST UPDATE")
    session.query(Requests).filter_by(host='cdd').update({"host": "UPDATED"})


def request_query():
    print("REQUEST QUERY")
    for instance in session.query(Requests):
        print(instance.host)


def request_delete():
    print("REQUEST DELETE")
    session.query(Requests).filter(Requests.host == 'UPDATED').delete()


