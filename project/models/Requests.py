from sqlalchemy import Column, Integer, Text
from project.database.Database import Base


class Requests(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    datetime = Column(Text)
    tool = Column(Text)
    first_line_format = Column(Text)
    method = Column(Text)
    scheme = Column(Text)
    host = Column(Text)
    port = Column(Text)
    path = Column(Text)
    http_version = Column(Text)
    headers = Column(Text)
    content = Column(Text)
    timestamp_start = Column(Text)
    timestamp_end = Column(Text)

    def __init__(self,
                 datetime=None,
                 tool=None,
                 first_line_format=None,
                 method=None,
                 scheme=None,
                 host=None,
                 port=None,
                 path=None,
                 http_version=None,
                 headers=None,
                 content=None,
                 timestamp_start=None,
                 timestamp_end=None):
        self.datetime = datetime
        self.tool = tool
        self.first_line_format = first_line_format
        self.method = method
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path
        self.http_version = http_version
        self.headers = headers
        self.content = content
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end

    def __repr__(self):
        return '<Request %r>' % self.name
