#!/usr/bin/env python
import json
import os
import requests

from flask import Flask, jsonify, request

app = Flask(__name__)

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
    return 'Hello World! ' + os.environ.get('TEST_KEY', None)


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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.debug = True
    #app.run(host='127.0.0.1', port=5000)
