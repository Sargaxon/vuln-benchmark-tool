import pandas as pd
import matplotlib.pyplot as plt
from project.models.Response import Response
from project.models.Request import Request

tool = "zaproxy"
app = "flask"


def request_method():
    plt.figure(1)

    # REQUEST TYPE (METHOD) CHART:
    plt.subplot(211)
    count_get = Request.query.filter(Request.method == 'GET').count()
    count_post = Request.query.filter(Request.method == 'POST').count()

    series = pd.Series(data=[count_get, count_post], index=['GET', 'POST'], name="Request type (method)")
    series.plot.pie(subplots=True, labels=["GET", "POST"], colors=['b', 'r'], autopct='%.2f', fontsize=20,
                    figsize=(6, 6))
    plt.title("%s - %s" % (tool, app))

    # RESPONSE HTTP STATUS CODES CHART
    plt.subplot(212)
    http_status_codes = ['200', '301', '302', '404', '405', '429']
    counter_results = []
    for i in range(0, 6):
        counter = Response.query.filter(Response.status_code == http_status_codes[i]).count()
        counter_results.append(counter)

    series2 = pd.Series(data=counter_results, index=http_status_codes, name="Response HTTP status codes")
    series2.plot.pie(subplots=True, labels=http_status_codes, fontsize=10, figsize=(6, 6))
    plt.title("%s - %s" % (tool, app))

    # plt.show()
