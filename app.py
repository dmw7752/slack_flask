#!/usr/bin/env python
import json
import os
import requests
import redis
import re
import sys
import logging

from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Lets get some logs out of heroku!
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Setup connection to redis
if os.environ.get('RUNNING_IN_HEROKU'):
    redis = redis.from_url(os.environ.get('REDIS_URL'))
else:
    redis = redis.StrictRedis(host='localhost', port=6379, db=0)

# Authorization decorator. If you decorate a function with this it will only
# be able to execute if the slack api token is passed with the call.
# Only works when running in heroku so that curl testing is easier during development.
def require_slack_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if os.environ.get('RUNNING_IN_HEROKU'):
            if request.form.get('token') not in os.environ.get('SLACK_API_KEYS').split(","):
                return '401 - Not Authorized', 401
        return f(*args, **kwargs)
    return decorated_function

def get_stock(ids):
    """Use Google's Finance API to retrieve stock prices"""

    # Retrieving all the stock prices at once is much faster
    # We are required to use the "id" in this case.
    url = "https://finance.google.com/finance/data?dp=mra&catid=all&output=json&cid=%s" % ids

    r = requests.get(url)
    response = r.json()
    prices = []
    for element in response['company']['related']['rows']:
        prices.append(
            (
                # Ticker symbol
                element['values'][1],
                # Current price
                element['values'][6],
                # Change
                element['values'][7]
            )
        )
    return prices


def get_crypto():
    """Use coinbase API to return current price of BTC"""

    url = "https://api.coinbase.com/v2/prices/spot?currency=USD"

    r = requests.get(url)
    j = json.loads(r.text)
    price = j['data']['amount']
    return price


@app.route('/')
def main():
    return 'Welcome to nocbot!'


@app.route('/stock', methods=['POST'])
def stock():
    # TODO: Move this into a config.
    # ID retrived from finance.google.com/finance?q=SYMBOL&output=json
    tickers = {'BOX':'1011797299780085', 'MSFT':'358464'}
    ids = (',').join(tickers.values())

    prices = get_stock(ids)
    stocks = ''
    for price in prices:
        stocks += '%s: $%s (%s) ' % (price[0], price[1], price[2])
        if '+' in price[2]:
            stocks += ':chart_with_upwards_trend:\n'
        else:
            stocks += ':chart_with_downwards_trend:\n'
    btc = get_crypto()
    stocks += 'BTC: $%s' % btc

    response = jsonify(text=stocks)
    return response

@require_slack_token
@app.route('/plusplus/addremove', methods=['POST'])
def plusplus_add_remove():
    text = request.form.get('text')
    try:
        m = re.match(r'.*\s?@(.*)\s?(\+\+|--)', text)
        key = m.group(1)
        operation = m.group(2)
    # TODO: This really needs to be a better catch
    # and more importantly, not do anything if it doenst match
    except:
        return "There was a problem with the regex"

    key = key.strip().lower()
    current_value = redis.get(key)
    if current_value:
        if operation == "++":
            new_value = int(current_value) + 1
            redis.set(key, new_value)
        else:
            new_value = int(current_value) - 1
            redis.set(key, new_value)
    else:
        if operation == "++":
            new_value = 1
            redis.set(key, 1)
        else:
            new_value = -1
            redis.set(key, -1)

    response_text = "{} has {} points!".format(key, new_value)
    json_response = jsonify(text=response_text)
    return json_response

"""
@app.route('/plusplus/leaderboard', methods=['POST'])
@require_slack_token
def plusplus_leaderboard():
    leaders = {}
    for key in redis.scan_iter("*"):
        leaders[key] = redis.get(key)
    leaders_sorted = []
    for key, value in sorted(leaders.iteritems(), key=lambda (k,v): (v,k),reverse=True):
        leaders_sorted.append("{}: {}".format(key, value))

    # TODO: I gotta figure out how to jsonify a list or a dict
    # but wanna push this and test other stuff first.
    return "DONE\n"
"""

if __name__ == '__main__':
    if os.environ.get('RUNNING_IN_HEROKU'):
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:
        app.debug = True
        app.run(host='127.0.0.1', port=5000)
