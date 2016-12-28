#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "apagado":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    time = makeYqlQuery(req)
    if time is None:
        return {}
    
    res = makeWebhookResult(time)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    time = parameters.get("time")
    if time is None:
        return None

    return "time"


def makeWebhookResult(time):
    # print(json.dumps(item, indent=4))

    speech = "hello" + time

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
