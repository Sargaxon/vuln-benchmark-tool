import io
from collections import OrderedDict
from operator import itemgetter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy.orm as orm
from matplotlib.font_manager import FontProperties
from sqlalchemy import and_
from flask import Markup, flash

from project.models.RequestHeader import RequestHeader
from project.models.Response import Response
from project.models.Request import Request
from sqlalchemy.sql import compiler
from psycopg2.extensions import adapt as sqlescape

# tool = "zaproxy"
app = "flask"


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

    return my_autopct


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
