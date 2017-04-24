from collections import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import and_

from project import tools
from project.models.RequestHeader import RequestHeader
from project.models.Request import Request

# tool = "zaproxy"
app = "flask"
request_fields = ['method', 'content']
skip_header_fields = ['accept_encoding', 'accept_datetime', 'h_authorization', 'content_md5', 'date', 'expect',
                      'forwarded', 'h_from', 'if_match', 'if_modified_since', 'if_none_match', 'if_range',
                      'if_unmodified_since', 'max_forwards', 'origin', 'proxy_authorization', 'proxy_connection',
                      'range', 'referer', 'te', 'upgrade', 'via', 'warning']

request_header_fields = [
    'Accept', 'Accept-Charset', 'Accept-Encoding', 'Accept-Language', 'Accept-Datetime',
    'Connection', 'H-Authorization', 'Cache-Control', 'Cookie', 'Content-Length',
    'Content-MD5', 'Content-Type', 'Date', 'Expect', 'Forwarded', 'H-From', 'Host',
    'If-Match', 'If-Modified-Since', 'If-None-Match', 'If-Range', 'If-Unmodified-Since',
    'Max-Forwards', 'Origin', 'Pragma', 'Proxy-Authorization', 'Proxy-Connection', 'Range',
    'Referer', 'TE', 'User-Agent', 'Upgrade', 'Via', 'Warning']


def request_comparison():
    # PIE COMPARISON CHART
    plt.figure(1)
    data = {}
    for i in range(1, len(tools)):
        data[tools[i][1]] = Request.query.filter(Request.tool == tools[i][0]).count()

    data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True))

    series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="")
    series.plot.pie(subplots=True, labels=None, labeldistance=.5,
                    fontsize=15, figsize=(6, 6), legend=True)
    L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
    for i in range(0, len(data.items())):
        L.get_texts()[i].set_text("{0} ({1}%)[{2}]"
                                  .format(list(data.keys())[i],
                                          round(100 * float(list(data.values())[i]) / sum(data.values()), 2),
                                          list(data.values())[i]))
    plt.subplots_adjust(right=0.8)
    plt.title("Total number of tests ratio")
    plt.savefig('images/allPie_RequestsRatio.png', bbox_inches='tight')
    plt.clf()

    # BAR COMPARISON CHART
    plt.figure(2)
    df = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys())
    ax = df.plot(kind='bar', title="Sum of executed requests comparison", figsize=(15, 10), fontsize=12)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), xy=(p.get_x(), p.get_height()), fontsize=15)
    ax.set_xlabel("Tool name", fontsize=15)
    ax.set_ylabel("Number of executed tests", fontsize=15)
    plt.savefig('images/allBar_RequestsCount.png', bbox_inches='tight')
    plt.clf()

    # REQUEST FIELDS - ALL TOOLS COMPARISON:
    for i in range(0, len(request_fields)):
        field = request_fields[i].lower()
        plt.figure(i)
        data = {}
        for k in range(1, len(tools)):
            data[tools[k][0]] = 0
            query = Request.query.filter(Request.tool == tools[k][0]).distinct(field)
            for r in query:
                if getattr(r, field) is None:
                    continue
                else:
                    data[tools[k][0]] += Request.query.filter(and_(getattr(Request, field) == getattr(r, field)),
                                                              (Request.tool == tools[k][0])).count()

            data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

        series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                           name="Request type (%s)" % field)
        series.plot.pie(subplots=True, labels=None, labeldistance=.5,  # autopct="%.2f", pctdistance=.7,
                        fontsize=8, figsize=(6, 6), legend=True)
        L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
        for j in range(0, len(data.items())):
            L.get_texts()[j].set_text("{0} ({1}%)[{2}]"
                                      .format(list(data.keys())[j][:15],
                                              round(100 * float(list(data.values())[j]) / sum(data.values()), 2),
                                              list(data.values())[j]))

        plt.subplots_adjust(right=0.8)
        plt.title("Tested requests %s ratio" % field)
        plt.savefig('images/all_%s.png' % field, bbox_inches='tight')
        plt.clf()

    # REQUEST HEADER FIELDS - ALL TOOLS COMPARISON:
    for i in range(0, len(request_header_fields)):
        field = request_header_fields[i].lower().replace("-", "_")
        if field in skip_header_fields:
            continue
        plt.figure(i)
        data = {}
        for k in range(1, len(tools)):
            data[tools[k][0]] = 0
            query = RequestHeader.query.filter(RequestHeader.tool == tools[k][0]).distinct(field)
            for r in query:
                if getattr(r, field) is None:
                    continue
                else:
                    data[tools[k][0]] += RequestHeader.query.filter(and_(getattr(RequestHeader, field) == getattr(r, field)),
                                                                        (RequestHeader.tool == tools[k][0])).count()

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

        series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                           name="RequestHeader type (%s)" % field)
        series.plot.pie(subplots=True, labels=None, labeldistance=.5,  # autopct="%.2f", pctdistance=.7,
                        fontsize=8, figsize=(6, 6), legend=True)
        L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
        for j in range(0, len(data.items())):
            L.get_texts()[j].set_text("{0} ({1}%)[{2}]"
                                      .format(list(data.keys())[j][:15],
                                              round(100 * float(list(data.values())[j]) / sum(data.values()), 2),
                                              list(data.values())[j]))
        plt.subplots_adjust(right=0.8)
        plt.title("Tested Requests Headers accept ratio")
        plt.savefig('images/allPie_{0}.png'.format(field), bbox_inches='tight')
        plt.clf()


def request_method(tool):
    i = 0
    # req_sum = Request.query.filter(Request.tool == tool).count()
    # message = Markup("<p><b>General</b><br>"
    #                  "Requests sum: {0}<br>"
    #                  "Requests per second: {1}</p>".format(req_sum, 0))  # to do
    # flash(message)

    # REQUESTS
    for i in range(0, len(request_fields)):
        field = request_fields[i].lower()
        plt.figure(i)
        data = {}
        query = Request.query.filter(Request.tool == tool).distinct(field)
        for r in query:
            parse = str(getattr(r, field) or 'null')
            parse = parse.replace('"', "").strip()
            query_count = Request.query.filter(and_(getattr(Request, field) == getattr(r, field)),
                                               (Request.tool == tool)).count()
            if parse in data:
                data[parse] += query_count
            else:
                data[parse] = query_count

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

        series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(), name="Request type (method)")
        series.plot.pie(subplots=True, labels=None, labeldistance=.5,  # autopct="%.2f", pctdistance=.7,
                        fontsize=8, figsize=(6, 6), legend=True)
        L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
        for j in range(0, len(data.items())):
            L.get_texts()[j].set_text("{0} ({1}%)[{2}]"
                                      .format(list(data.keys())[j][:15],
                                              round(100 * float(list(data.values())[j]) / sum(data.values()), 2),
                                              list(data.values())[j]))
        plt.subplots_adjust(right=0.8)
        plt.title("%s - %s" % (tool, app))
        plt.savefig('images/{0}_{1}.png'.format(tool, field), bbox_inches='tight')
        plt.clf()

    # REQUEST HEADERS
    for i in range(0, len(request_header_fields)):
        field = request_header_fields[i].lower().replace("-", "_")
        if field in skip_header_fields:
            continue
        plt.figure(i)
        data = {}
        query = RequestHeader.query.filter(RequestHeader.tool == tool).distinct(field)
        for r in query:
            parse = str(getattr(r, field) or 'null')
            query_count = RequestHeader.query.filter(and_(getattr(RequestHeader, field) == getattr(r, field)),
                                                     (RequestHeader.tool == tool)).count()
            if parse in data:
                data[parse] += query_count
            else:
                data[parse] = query_count

        data = OrderedDict(sorted(data.items(), key=lambda t: t[1], reverse=True)[:15])

        series = pd.Series(data={k: int(v) for k, v in data.items()}, index=data.keys(),
                           name="RequestHeader (%s)" % field)
        series.plot.pie(subplots=True, labels=None, labeldistance=.5,  # autopct="%.2f", pctdistance=.7,
                        fontsize=8, figsize=(6, 6), legend=True)
        L = plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", labels=series.index)
        for j in range(0, len(data.items())):
            L.get_texts()[j].set_text("{0} ({1}%)[{2}]"
                                      .format(list(data.keys())[j][:15],
                                              round(100 * float(list(data.values())[j]) / sum(data.values()), 2),
                                              list(data.values())[j]))
        plt.subplots_adjust(right=0.8)
        plt.title("%s - %s" % (tool, app))
        plt.savefig('images/{0}{1}_{2}.png'.format(tool, i, field), bbox_inches='tight')
        plt.clf()
