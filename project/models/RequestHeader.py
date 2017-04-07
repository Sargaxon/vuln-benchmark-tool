from sqlalchemy import Column, Integer, Text
from project.database.Database import Base, session


class RequestHeader(Base):
    __tablename__ = 'requests_headers'

    id_request = Column(Integer, primary_key=True)
    accept = Column(Text)
    accept_charset = Column(Text)
    accept_encoding = Column(Text)
    accept_language = Column(Text)
    accept_datetime = Column(Text)
    connection = Column(Text)
    h_authorization = Column(Text)
    cache_control = Column(Text)
    cookie = Column(Text)
    content_length = Column(Text)
    content_md5 = Column(Text)
    content_type = Column(Text)
    date = Column(Text)
    expect = Column(Text)
    forwarded = Column(Text)
    h_from = Column(Text)
    host = Column(Text)
    if_match = Column(Text)
    if_modified_since = Column(Text)
    if_none_match = Column(Text)
    if_range = Column(Text)
    if_unmodified_since = Column(Text)
    max_forwards = Column(Text)
    origin = Column(Text)
    pragma = Column(Text)
    proxy_authorization = Column(Text)
    proxy_connection = Column(Text)
    range = Column(Text)
    referer = Column(Text)
    te = Column(Text)
    user_agent = Column(Text)
    upgrade = Column(Text)
    via = Column(Text)
    warning = Column(Text)

    def __init__(self,
                 accept=None,
                 accept_charset=None,
                 accept_encoding=None,
                 accept_language=None,
                 accept_datetime=None,
                 connection=None,
                 h_authorization=None,
                 cache_control=None,
                 cookie=None,
                 content_length=None,
                 content_md5=None,
                 content_type=None,
                 date=None,
                 expect=None,
                 forwarded=None,
                 h_from=None,
                 host=None,
                 if_match=None,
                 if_modified_since=None,
                 if_none_match=None,
                 if_range=None,
                 if_unmodified_since=None,
                 max_forwards=None,
                 origin=None,
                 pragma=None,
                 proxy_authorization=None,
                 proxy_connection=None,
                 range=None,
                 referer=None,
                 te=None,
                 user_agent=None,
                 upgrade=None,
                 via=None,
                 warning=None):
        self.accept = accept
        self.accept_charset = accept_charset
        self.accept_encoding = accept_encoding
        self.accept_language = accept_language
        self.accept_datetime = accept_datetime
        self.connection = connection
        self.h_authorization = h_authorization
        self.cache_control = cache_control
        self.cookie = cookie
        self.content_length = content_length
        self.content_md5 = content_md5
        self.content_type = content_type
        self.date = date
        self.expect = expect
        self.forwarded = forwarded
        self.h_from = h_from
        self.host = host
        self.if_match = if_match
        self.if_modified_since = if_modified_since
        self.if_none_match = if_none_match
        self.if_range = if_range
        self.if_unmodified_since = if_unmodified_since
        self.max_forwards = max_forwards
        self.origin = origin
        self.pragma = pragma
        self.proxy_authorization = proxy_authorization
        self.proxy_connection = proxy_connection
        self.range = range
        self.referer = referer
        self.te = te
        self.user_agent = user_agent
        self.upgrade = upgrade
        self.via = via
        self.warning = warning

    def insert(self):
        session.add(self)
        session.commit()

    @staticmethod
    def update():
        session.commit()

    @staticmethod
    def find_one(entity_id):
        return RequestHeader.query.filter(RequestHeader.id_request == entity_id).first()

    @staticmethod
    def delete(entity_id):
        RequestHeader.query.filter(RequestHeader.id_request == entity_id).delete()
        session.commit()
