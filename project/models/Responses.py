from sqlalchemy import Column, Integer, Text
from project.database.Database import Base


class Responses(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    datetime = Column(Text)
    app = Column(Text)
    http_version = Column(Text)
    status_code = Column(Text)
    reason = Column(Text)
    headers = Column(Text)
    content = Column(Text)
    timestamp_start = Column(Text)
    timestamp_end = Column(Text)

    def __init__(self,
                 datetime=None,
                 app=None,
                 http_version=None,
                 status_code=None,
                 reason=None,
                 headers=None,
                 content=None,
                 timestamp_start=None,
                 timestamp_end=None):
        self.datetime = datetime
        self.app = app
        self.http_version = http_version
        self.status_code = status_code
        self.reason = reason
        self.headers = headers
        self.content = content
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end

    def __repr__(self):
        return '<Response %r>' % self.name
