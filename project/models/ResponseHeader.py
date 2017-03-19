from sqlalchemy import Column, Integer, Text
from project.database.Database import Base, session


class ResponseHeader(Base):
    __tablename__ = "responses_headers"

    id_response = Column(Integer, primary_key=True)
    access_control_allow_origin = Column(Text)
    accept_patch = Column(Text)
    accept_ranges = Column(Text)
    age = Column(Text)
    allow = Column(Text)
    alt_svc = Column(Text)
    cache_control = Column(Text)
    connection = Column(Text)
    content_disposition = Column(Text)
    content_encoding = Column(Text)
    content_language = Column(Text)
    content_length = Column(Text)
    content_location = Column(Text)
    content_md5 = Column(Text)
    content_range = Column(Text)
    content_type = Column(Text)
    date = Column(Text)
    etag = Column(Text)
    expires = Column(Text)
    last_modified = Column(Text)
    link = Column(Text)
    location = Column(Text)
    p3p = Column(Text)
    pragma = Column(Text)
    proxy_authenticate = Column(Text)
    public_key_pins = Column(Text)
    refresh = Column(Text)
    retry_after = Column(Text)
    server = Column(Text)
    set_cookie = Column(Text)
    status = Column(Text)
    strict_transport_security = Column(Text)
    trailer = Column(Text)
    transfer_encoding = Column(Text)
    tsv = Column(Text)
    upgrade = Column(Text)
    vary = Column(Text)
    via = Column(Text)
    warning = Column(Text)
    www_authenticate = Column(Text)
    x_frame_options = Column(Text)

    def __init__(self,
                 access_control_allow_origin=None,
                 accept_patch=None,
                 accept_ranges=None,
                 age=None,
                 allow=None,
                 alt_svc=None,
                 cache_control=None,
                 connection=None,
                 content_disposition=None,
                 content_encoding=None,
                 content_language=None,
                 content_length=None,
                 content_location=None,
                 content_md5=None,
                 content_range=None,
                 content_type=None,
                 date=None,
                 etag=None,
                 expires=None,
                 last_modified=None,
                 link=None,
                 location=None,
                 p3p=None,
                 pragma=None,
                 proxy_authenticate=None,
                 public_key_pins=None,
                 refresh=None,
                 retry_after=None,
                 server=None,
                 set_cookie=None,
                 status=None,
                 strict_transport_security=None,
                 trailer=None,
                 transfer_encoding=None,
                 tsv=None,
                 upgrade=None,
                 vary=None,
                 via=None,
                 warning=None,
                 www_authenticate=None,
                 x_frame_options=None):
        self.access_control_allow_origin = access_control_allow_origin
        self.accept_patch = accept_patch
        self.accept_ranges = accept_ranges
        self.age = age
        self.allow = allow
        self.alt_svc = alt_svc
        self.cache_control = cache_control
        self.connection = connection
        self.content_disposition = content_disposition
        self.content_encoding = content_encoding
        self.content_language = content_language
        self.content_length = content_length
        self.content_location = content_location
        self.content_md5 = content_md5
        self.content_range = content_range
        self.content_type = content_type
        self.date = date
        self.etag = etag
        self.expires = expires
        self.last_modified = last_modified
        self.link = link
        self.location = location
        self.p3p = p3p
        self.pragma = pragma
        self.proxy_authenticate = proxy_authenticate
        self.public_key_pins = public_key_pins
        self.refresh = refresh
        self.retry_after = retry_after
        self.server = server
        self.set_cookie = set_cookie
        self.status = status
        self.strict_transport_security = strict_transport_security
        self.trailer = trailer
        self.transfer_encoding = transfer_encoding
        self.tsv = tsv
        self.upgrade = upgrade
        self.vary = vary
        self.via = via
        self.warning = warning
        self.www_authenticate = www_authenticate
        self.x_frame_options = x_frame_options

    def insert(self):
        session.add(self)
        session.commit()

    @staticmethod
    def update():
        session.commit()

    @staticmethod
    def find_one(entity_id):
        return ResponseHeader.query.filter(ResponseHeader.id == entity_id).first()

    def delete(self):
        ResponseHeader.query.filter(ResponseHeader.id == self.id).delete()
        session.commit()
