import io
from collections import OrderedDict
from operator import itemgetter
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy.orm as orm
from matplotlib.font_manager import FontProperties
from sqlalchemy import and_
from flask import Markup, flash

from project import tools
from project.models.RequestHeader import RequestHeader
from project.models.Response import Response
from project.models.Request import Request
from sqlalchemy.sql import compiler
from psycopg2.extensions import adapt as sqlescape

# tool = "zaproxy"
app = "flask"


def request_comparison():
    # PIE COMPARISON CHART
    plt.figure(1)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][1]] = Request.query.filter(Request.tool == tools[i][0]).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=15, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Total number of tests ratio")
    plt.savefig('allPieRequestsRatio.jpg', bbox_inches='tight')
    plt.clf()

    # BAR COMPARISON CHART
    plt.figure(2)
    df = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys())
    ax = df.plot(kind='bar', title="Sum of executed requests comparison", figsize=(15, 10), fontsize=12)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()), fontsize=15)
    ax.set_xlabel("Tool name", fontsize=15)
    ax.set_ylabel("Number of executed tests", fontsize=15)
    plt.savefig('allBarRequestsCount.jpg', bbox_inches='tight')
    plt.clf()





    # REQUESTCOMPARISON - METHOD RATIO CHART:
    plt.figure(3)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = Request.query.filter(Request.tool == tools[i][0]).distinct('method')
        for r in query:
            if r.method is None:
                continue
            else:
                data[tools[i][0]] += Request.query.filter(and_(Request.method == r.method), (Request.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (method)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested requests methods ratio")
    plt.savefig('allPieMethod.jpg', bbox_inches='tight')
    plt.clf()

# REQUESTCOMPARISON - content RATIO CHART:
    plt.figure(4)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = Request.query.filter(Request.tool == tools[i][0]).distinct('content')
        for r in query:
            if r.content is None:
                continue
            else:
                data[tools[i][0]] += Request.query.filter(and_(Request.content == r.content), (Request.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (content)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested requests content ratio")
    plt.savefig('allPie_content.jpg', bbox_inches='tight')
    plt.clf()

# REQUESTCOMPARISON - accept RATIO CHART:
    plt.figure(5)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('accept')
        for r in query:
            if r.accept is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.accept == r.accept), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (accept)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers accept ratio")
    plt.savefig('allPie_accept.jpg', bbox_inches='tight')
    plt.clf()


# REQUESTCOMPARISON - accept_charset RATIO CHART:
    plt.figure(5)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('accept_charset')
        for r in query:
            if r.accept_charset is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.accept_charset == r.accept_charset), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (accept_charset)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers accept_charset ratio")
    plt.savefig('allPie_accept_charset.jpg', bbox_inches='tight')
    plt.clf()


# REQUESTCOMPARISON - connection RATIO CHART:
    plt.figure(6)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('connection')
        for r in query:
            if r.connection is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.connection == r.connection), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (connection)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers connection ratio")
    plt.savefig('allPie_connection.jpg', bbox_inches='tight')
    plt.clf()


# REQUESTCOMPARISON - cache_control RATIO CHART:
    plt.figure(7)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('cache_control')
        for r in query:
            if r.cache_control is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.cache_control == r.cache_control), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (cache_control)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers cache_control ratio")
    plt.savefig('allPie_cache_control.jpg', bbox_inches='tight')
    plt.clf()

# REQUESTCOMPARISON - content_length RATIO CHART:
    plt.figure(8)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('content_length')
        for r in query:
            if r.content_length is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.content_length == r.content_length), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (content_length)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers content_length ratio")
    plt.savefig('allPie_content_length.jpg', bbox_inches='tight')
    plt.clf()

# REQUESTCOMPARISON - user_agent RATIO CHART:
    plt.figure(9)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('content_type')
        for r in query:
            if r.content_type is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.content_type == r.content_type), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (content_type)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers content_type ratio")
    plt.savefig('allPie_content_type.jpg', bbox_inches='tight')
    plt.clf()


# REQUESTCOMPARISON - host RATIO CHART:
    plt.figure(10)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('host')
        for r in query:
            if r.host is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.host == r.host), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (host)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers host ratio")
    plt.savefig('allPie_host.jpg', bbox_inches='tight')
    plt.clf()

# REQUESTCOMPARISON - pragma RATIO CHART:
    plt.figure(11)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('pragma')
        for r in query:
            if r.pragma is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.pragma == r.pragma), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (pragma)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers pragma ratio")
    plt.savefig('allPie_pragma.jpg', bbox_inches='tight')
    plt.clf()


# REQUESTCOMPARISON - user_agent RATIO CHART:
    plt.figure(12)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('user_agent')
        for r in query:
            if r.user_agent is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.user_agent == r.user_agent), (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader type (user_agent)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers user_agent ratio")
    plt.savefig('allPie_user_agent.jpg', bbox_inches='tight')
    plt.clf()

    # REQUESTCOMPARISON - cookie RATIO CHART:
    plt.figure(13)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][0]] = 0
        query = RequestHeader.query.filter(RequestHeader.tool == tools[i][0]).distinct('cookie')
        for r in query:
            if r.cookie is None:
                continue
            else:
                data[tools[i][0]] += RequestHeader.query.filter(and_(RequestHeader.cookie == r.cookie),
                                                                (RequestHeader.tool == tools[i][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader type (cookie)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("Tested Requests Headers cookie ratio")
    plt.savefig('allPie_cookie.jpg', bbox_inches='tight')
    plt.clf()


def request_method(tool):
    # req_sum = Request.query.filter(Request.tool == tool).count()
    # message = Markup("<p><b>General</b><br>"
    #                  "Requests sum: {0}<br>"
    #                  "Requests per second: {1}</p>".format(req_sum, 0))  # to do
    # flash(message)

    # REQUEST - METHOD RATIO CHART:
    plt.figure(1)
    data = {}
    query = Request.query.filter(Request.tool == tool).distinct('method')
    for r in query:
        # print("METHoD: " + str(r.method.replace('"', "")))
        # print("COUNT: " + str(Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()))
        parse = str(r.method or 'null')
        parse = parse.replace('"', "").strip()
        if parse in data:
            data[parse] += Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()
        else:
            data[parse] = Request.query.filter(and_(Request.method == r.method), (Request.tool == tool)).count()

    # print("\n***DICT***")
    # for i, v in data.items():
    #     print(i, v)

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (method)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s1.jpg' % tool, bbox_inches='tight')
    plt.clf()


  #  REQUEST - content RATIO CHART:
    plt.figure(2)
    data = {}
    query = Request.query.filter(Request.tool == tool).distinct('content')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.content or 'null')
        if parse in data:
            data[parse] += Request.query.filter(and_(Request.content == r.content), (Request.tool == tool)).count()
        else:
            data[parse] = Request.query.filter(and_(Request.content == r.content), (Request.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (content)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):

        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s2.jpg' % tool, bbox_inches='tight')
    plt.clf()

#  REQUESTHEADER - ACCEPT RATIO CHART:
    plt.figure(3)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.accept or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept == r.accept), (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept == r.accept), (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader (accept)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):

        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s3.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - ACCEPT CHARSET RATIO CHART:
    plt.figure(4)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept_charset')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.accept_charset or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept_charset == r.accept_charset),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept_charset == r.accept_charset),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader (accept_charset)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s4.jpg' % tool, bbox_inches='tight')
    plt.clf()


   #  REQUESTHEADER - ACCEPT CHARSET RATIO CHART:
    plt.figure(5)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('accept_encoding')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.accept_encoding or 'null')
        parse = parse.replace(' ', '')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.accept_encoding == r.accept_encoding),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.accept_encoding == r.accept_encoding),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader (accept_encoding)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s5.jpg' % tool, bbox_inches='tight')
    plt.clf()


 #  REQUESTHEADER - CONNECTION RATIO CHART:
    plt.figure(6)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('connection')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.connection or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.connection == r.connection),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.connection == r.connection),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="RequestHeader (connection)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s6.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - cache_control RATIO CHART:
    plt.figure(7)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('cache_control')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.cache_control or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.cache_control == r.cache_control),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.cache_control == r.cache_control),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (cache_control)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s7.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - content_length RATIO CHART:
    plt.figure(8)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('content_length')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.content_length or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.content_length == r.content_length),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.content_length == r.content_length),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (content_length)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s8.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - content_type RATIO CHART:
    plt.figure(9)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('content_type')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.content_type or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.content_type == r.content_type),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.content_type == r.content_type),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (content_type)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s9.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - host RATIO CHART:
    plt.figure(10)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('host')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.host or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.host == r.host),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.host == r.host),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (host)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s10.jpg' % tool, bbox_inches='tight')
    plt.clf()


    #  REQUESTHEADER - pragma RATIO CHART:
    plt.figure(11)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('pragma')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.pragma or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.pragma == r.pragma),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.pragma == r.pragma),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (pragma)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s11.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - user_agent RATIO CHART:
    plt.figure(12)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('user_agent')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.user_agent or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.user_agent == r.user_agent),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.user_agent == r.user_agent),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (user_agent)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s12.jpg' % tool, bbox_inches='tight')
    plt.clf()

    #  REQUESTHEADER - cookie RATIO CHART:
    plt.figure(13)
    data = {}
    query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct('cookie')
    for r in query:
        # parse = r.content.replace('"', "").strip()
        parse = str(r.cookie or 'null')
        if parse in data:
            data[parse] += RequestHeader.query.filter(and_(RequestHeader.cookie == r.cookie),
                                                      (RequestHeader.tool == tool)).count()
        else:
            data[parse] = RequestHeader.query.filter(and_(RequestHeader.cookie == r.cookie),
                                                     (RequestHeader.tool == tool)).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                       name="RequestHeader (cookie)")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5, autopct="%.2f", pctdistance=.7,
                    fontsize=8, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1})".format(list(data.keys())[i][:15], list(data.values())[i]))

    plt.subplots_adjust(right=0.8)
    plt.title("%s - %s" % (tool, app))
    plt.savefig('%s13.jpg' % tool, bbox_inches='tight')
    plt.clf()


request_comparison()
