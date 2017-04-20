import io
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy.orm as orm
from sqlalchemy import and_
from flask import Markup, flash

from project.models.RequestHeader import RequestHeader
from project.models.Response import Response
from project.models.Request import Request
from sqlalchemy.sql import compiler
from psycopg2.extensions import adapt as sqlescape
# tool = "zaproxy"
app = "flask"


def request_method(tool):
    req_sum = Request.query.filter(Request.tool == tool).count()
    message = Markup("<p><b>General</b><br>"
                     "Requests sum: {0}<br>"
                     "Requests per second: {1}</p>".format(req_sum, 0))  # to do
    flash(message)

    # REQUEST - METHOD RATIO CHART:
    plt.figure(1)
    data = {}
    query = Request.query.filter(Request.tool == tool).distinct('method')
    for r in query:
        # print("METHoD: " + str(r.method.replace('"', "")))
        # print("COUNT: " + str(Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()))
        parse = r.method.replace('"', "").strip()
        if parse in data:
            data[parse] += Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()
        else:
            data[parse] = Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    # print("\n***DICT***")
    # for i, v in data.items():
    #     print(i, v)

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (method)")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s1.jpg' % tool)
    plt.clf()

    # REQUEST - content RATIO CHART:
    plt.figure(2)
    data = {}
    query = Request.query.filter(Request.tool == tool).distinct('content')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = r.content
        if parse in data:
            data[parse] += Request.query.filter(and_(Request.content == r.content), (Request.tool == tool)).count()
        else:
            data[parse] = Request.query.filter(and_(Request.content == r.content), (Request.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request content")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s2.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - ACCEPT RATIO CHART:
    plt.figure(3)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept')
    for r in query:
        # parse = r.path.replace('"', "").strip()

        parse = r.accept
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept == r.accept), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept == r.accept), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[acccept]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s3.jpg' % tool)
    plt.clf()


    # REQUESTHEADER - ACCEPT CHARSET RATIO CHART:
    plt.figure(4)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept_charset')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.accept_charset
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept_charset == r.accept_charset), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept_charset == r.accept_charset), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[accept_charset]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s4.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - ACCEPT ENCODING RATIO CHART:
    plt.figure(5)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept_encoding')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.accept_encoding
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept_encoding == r.accept_encoding), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept_encoding == r.accept_encoding), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[accept_encoding]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s5.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - CONNECTION RATIO CHART:
    plt.figure(6)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('connection')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.connection
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.connection == r.connection), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.connection == r.connection), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[connection]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s6.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - CACHE CONTROL RATIO CHART:
    plt.figure(7)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('cache_control')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.cache_control
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.cache_control == r.cache_control), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.cache_control == r.cache_control), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[cache_control]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s7.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - CONTENT LENGTH RATIO CHART:
    plt.figure(8)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('content_length')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.content_length
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.content_length == r.content_length), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.content_length == r.content_length), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[content_length]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s8.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - CONTENT TYPE RATIO CHART:
    plt.figure(9)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('content_type')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.content_type
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.content_type == r.content_type), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.content_type == r.content_type), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[content_type]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s9.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - HOST RATIO CHART:
    plt.figure(10)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('host')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.host
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.host == r.host), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.host == r.host), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[host]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s10.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - PRAGMA CHART:
    plt.figure(11)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('pragma')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.pragma
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.pragma == r.pragma), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.pragma == r.pragma), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[pragma]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s11.jpg' % tool)
    plt.clf()

    # REQUESTHEADER - USER AGENT CHART:
    plt.figure(11)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('user_agent')
    for r in query:
        # parse = r.path.replace('"', "").strip()
        parse = r.user_agent
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.user_agent == r.user_agent), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.user_agent == r.user_agent), (RequestHeader.tool == tool)).count()

    data["null"] = abs(Request.query.filter(Request.tool == tool).count() - sum(data.values()))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader[user_agent]")
    series.plot.pie(subplots=True, labels=None, autopct='%.2f', fontsize=8,
                    figsize=(6, 6), legend=True)
    plt.legend(loc='best', labels=series.index)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s11.jpg' % tool)
    plt.clf()
