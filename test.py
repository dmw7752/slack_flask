#!/usr/bin/env python
import urllib2
import json

def get_stock(exchange, symbol):
  url = "http://finance.google.com/finance/info?client=ig&q=%s:%s"%(exchange,symbol)
  u = urllib2.urlopen(url)
  content = u.read()

  obj = json.loads(content[3:])
  
  for key,val in obj[0].items():
    if key == 'l':
	  return val

if __name__ == '__main__':
  box = get_stock('NYSE', 'BOX')
  linkedin = get_stock('NYSE', 'LNKD')

  response = 'Box: ' + box + '\nLinkedin: ' + linkedin
  print response
