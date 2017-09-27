#!/usr/bin/env python
import json
import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

def get_stock(symbol):
  url = "http://finance.google.com/finance?q=%s&output=json" % symbol

  r = requests.get(url)
  for line in r.text.split("\n"):
    if "\"l\"" in line:
      last = line
      break

  # finance.google.com returns 200 even if stock
  # ticker doesn't exist. Error handling here instead.
  try:
      last = last.split('"')[1::2][1]
  except UnboundLocalError:
          last = '0.00'
  return last


def get_crypto():
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
  tickers = ['BOX', 'MSFT', 'SLACK']
  prices = [ (ticker, get_stock(ticker)) for ticker in tickers ]
  stocks = ''
  for price in prices:
      stocks += '%s: $%s\n' % (price[0], price[1])
  btc = get_crypto()
  stocks += 'BTC: $%s' % btc

  response = jsonify(text=stocks)
  return response

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  #app.debug = True
  #app.run(host='127.0.0.1', port=5000)
