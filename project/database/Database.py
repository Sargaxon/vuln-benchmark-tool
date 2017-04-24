from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from project import app


"""Connects to database engine (dialect+driver://username:password@host:port/database)"""
engine = create_engine(app.config['DATABASE'], encoding="utf-8")
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = session.query_property()


def db_create():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import project.models
    Base.metadata.create_all(bind=engine)

    db = engine.connect()
    db.execute('CREATE TABLE IF NOT EXISTS requests'
               '(id serial primary key, '
               'datetime text, '
               'tool text, '
               'first_line_format text, '
               'method text, '
               'scheme text, '
               'host text, '
               'port text, '
               'path text, '
               'http_version text, '
               'headers text, '
               'content text, '
               'timestamp_start text, '
               'timestamp_end text);')
    db.execute('CREATE TABLE IF NOT EXISTS responses(id serial primary key, '
               'datetime text, '
               'app text, '
               'http_version text, '
               'status_code text, '
               'reason text, '
               'headers text, '
               'content text, '
               'timestamp_start text, '
               'timestamp_end text);')
    db.execute('CREATE TABLE IF NOT EXISTS requests_headers(id_request int, '
               'accept text, '
               'accept_charset text, '
               'accept_encoding text, '
               'accept_language text, '
               'accept_datetime text, '
               'h_authorization text, '
               'cache_control text, '
               'connection text, '
               'cookie text, '
               'content_length text, '
               'content_md5 text, '
               'content_type text, '
               'date text, '
               'expect text, '
               'forwarded text, '
               'h_from text, '
               'host text, '
               'if_match text, '
               'if_modified_since text, '
               'if_none_match text, '
               'if_range text, '
               'if_unmodified_since text, '
               'max_forwards text, '
               'origin text, '
               'pragma text, '
               'proxy_authorization text, '
               'proxy_connection text, '
               'range text, '
               'referer  text, '
               'te text, '
               'user_agent text, '
               'upgrade text, '
               'via text, '
               'warning text, '
               'tool text'
               'foreign key (id_request) references requests(id))')
    db.execute('CREATE TABLE IF NOT EXISTS responses_headers(id_response serial, '
               'access_control_allow_origin text, '
               'accept_patch text, '
               'accept_ranges text, '
               'age text, '
               'allow text, alt_svc text, '
               'cache_control text, '
               'connection text, '
               'content_disposition text, '
               'content_encoding text, '
               'content_language text, '
               'content_length text, '
               'content_location text, '
               'content_md5 text, '
               'content_range text, '
               'content_type text, '
               'date text, '
               'etag text, '
               'expires text, '
               'last_modified text, '
               'link text, '
               'location text, '
               'p3p text, '
               'pragma text, '
               'proxy_authenticate text, '
               'public_key_pins text, '
               'refresh text, '
               'retry_after text, '
               'server text, '
               'set_cookie text, '
               'status text, '
               'strict_transport_security text, '
               'trailer text, '
               'transfer_encoding text, '
               'tsv text, '
               'upgrade text, vary text, '
               'via text, '
               'warning text, '
               'www_authenticate text, '
               'x_frame_options text, '
               'foreign key(id_response) references responses(id));')
    db.close()

    # db = engine.connect()
    # result = db.execute('select * from responses_headers')
    # for row in result:
    #     print(row['pragma'])
    # db.close()
