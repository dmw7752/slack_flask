#!/usr/bin/env python
# no op change
from bs4 import BeautifulSoup
import urllib2
import re
import os
import json
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

def get_traffic_info(url):
  usock = urllib2.urlopen(url)
  data = usock.read()
  usock.close()

  soup = BeautifulSoup(data)
  return soup.prettify('UTF-8')

def parse_html(html):
  match = re.search(r'In current.*', html, re.MULTILINE)
  return match.group(0)

def get_stock(exchange, symbol):
  url = "http://finance.google.com/finance/info?client=ig&q=%s:%s"%(exchange,symbol)
  u = urllib2.urlopen(url)
  content = u.read()

  obj = json.loads(content[3:])
  for key,val in obj[0].items():
    if key == 'l':
      return val

@app.route('/')
def main():
  return 'Hello World!'

@app.route('/traffic', methods=['POST'])
def traffic():
  to_work_html = get_traffic_info('https://www.google.com/maps/dir/448+Fathom+Dr,+San+Mateo,+CA+94404/Box,+El+Camino+Real,+Los+Altos,+CA/@37.4775139,-122.3671032,11z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x808f9ebe43184e3b:0xed88b704dbd9a898!2m2!1d-122.286044!2d37.568132!1m5!1m1!1s0x808fbaf3d1c8ade1:0xb619587d60dc1a37!2m2!1d-122.116445!2d37.402666')
  to_home_html = get_traffic_info('https://www.google.com/maps/dir/Box,+El+Camino+Real,+Los+Altos,+CA/448+Fathom+Dr,+San+Mateo,+CA+94404/@37.4656426,-122.3656023,11z/data=!3m1!4b1!4m13!4m12!1m5!1m1!1s0x808fbaf3d1c8ade1:0xb619587d60dc1a37!2m2!1d-122.116445!2d37.402666!1m5!1m1!1s0x808f9ebe43184e3b:0xed88b704dbd9a898!2m2!1d-122.286044!2d37.568132')

  to_work = parse_html(to_work_html)
  to_home = parse_html(to_home_html)

  commute = 'TO WORK - ' + to_work + '\nTO HOME - ' + to_home
  response = jsonify(text=commute)
  return response

@app.route('/stock', methods=['POST'])
def stock():
  box = get_stock('NYSE', 'BOX')
  linkedin = get_stock('NYSE', 'LNKD')

  stocks = 'Box: $' + box + '\nLinkedin: $' + linkedin
  response = jsonify(text=stocks)
  return response

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
  #app.debug = True
  #app.run(host='127.0.0.1', port=5000)
