#!/usr/bin/env python
import json
import os
import requests
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

def get_stock(exchange, symbol):
  url = "http://finance.google.com/finance?q=%s:%s&output=json"%(exchange,symbol)

  r = requests.get(url)
  for line in r.text.split("\n"):
    if "\"l\"" in line:
      last = line
      break

  last = last.split('"')[1::2][1]
  return last

@app.route('/')
def main():
  return 'Hello World! ' + TEST_KEY

@app.route('/stock', methods=['POST'])
def stock():
  box = get_stock('NYSE', 'BOX')
  msft = get_stock("NASDAQ", "MSFT")

  stocks = 'BOX: $' + box + '\nMSFT: $' + msft
  response = jsonify(text=stocks)
  return response

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  #app.debug = True
  #app.run(host='127.0.0.1', port=5000)
