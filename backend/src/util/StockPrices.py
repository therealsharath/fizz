#!/usr/bin/python3
# StockPrices.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import requests
from config import FMP_API_KEY as apikey
from AnalystRecommendations import getRecommendations

# parses JSON from HTTP GET request to financialmodlingprep API
def parseJSON(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
    return data

# parses JSON from HTTP GET request to financialmodlingprep API for price history
def getData105(url):
    data = parseJSON(url)
    prices = []
    length = 105

    for i in range(length):
        prices.append(data['historical'][i]['close'])

    return prices

# parses JSON from HTTP GET request to financialmodlingprep API for price at certain date
def getDataDatePrice(url, date):
    data = parseJSON(url)
    price = 0
    for i in data['historical']:
        if i['date'] == date:
            price = i['close']
            break

    while price == 0:
        i -= 1
        price = data['historical'][i]['close']
    return price

# parses JSON from HTTP GET request to financialmodlingprep API for stock industry
def getDataIndustry(url):
    data = parseJSON(url)
    return (data[0]['industry'], data[0]['sector'])

# parses JSON from HTTP GET request to financialmodlingprep API for gainers/losers
def getDataActiveStocks(url):
    data = parseJSON(url)
    actives = []
    length = 5

    for i in range(length):
        actives.append(data[i]['ticker'])

    return actives





########################################################################
# CALL THE BELOW FUNCTIONS!!! #
########################################################################

# checking whether or not asset exists
def assetExists(ticker):
    try:
        getRecommendations(ticker)
    except:
        return False
    return True

# returns list of last 105 closing prices of specified stock
def get105prices(ticker):
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?apikey=" + apikey)
    return getData105(url)

# returns price of stock at certain date
# date must be of format yyyy-mm-dd (eg. 2020-10-16)
def getDatePrice(ticker, date):
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?apikey=" + apikey)
    return getDataDatePrice(url, date)

# returns tuple for industry of the stock
# format: (industry, sector)
def getIndustry(ticker):
    url = ("https://financialmodelingprep.com/api/v3/profile/" + ticker + "?apikey=" + apikey)
    return getDataIndustry(url)

# returns list of top 5 gaining stocks
def getGainers():
    url = ("https://financialmodelingprep.com/api/v3/gainers?apikey=" + apikey)
    return getDataActiveStocks(url)

# returns list of top 5 losing stocks
def getLosers():
    url = ("https://financialmodelingprep.com/api/v3/losers?apikey=" + apikey)
    return getDataActiveStocks(url)

# returns TUPLE of top 5 gainers AND top 5 losers
# eg. (gainers, losers)
def getActives():
    return (getGainers(), getLosers())

# Gets description of asset
def getDescription(asset):
    url = 'https://financialmodelingprep.com/api/v3/profile/{asset}?apikey={apikey}'.format(asset=asset, apikey=apikey)
    response = requests.get(url)
    json_obj = json.loads(response.text)
    if not json_obj:
        return 'There is no known asset with that name.'

    sentences = json_obj[0]['description'].split('. ')
    sentence = 0
    while sentences[sentence + 1][0].islower():
        sentence += 1
    return {
        'description': '. '.join(sentences[:sentence + 1]) + '.',
        'industry': json_obj[0]['industry'],
        'sector': json_obj[0]['sector'],
        'price': json_obj[0]['price']
    }

# FOR DEBUGGING
# print(get105prices("AAPL"))
# print(getDatePrice("AAPL", "2020-09-14")) # should return $115.36
# print(assetExists("GOOGLSDFKASJDKFJ"))
# print(getActives())
