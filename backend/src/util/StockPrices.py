import json
import requests

def get_jsonparsed_data(url):

    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)

    prices = []

    length = 105

    for i in range(length):
        prices.append(data['historical'][i]['close'])

    return prices

def get105prices(ticker):
    url = ("https://financialmodelingprep.com/api/v3/historical-price-full/" + ticker + "?apikey=1778d0110e88aab90018dc63e8a3554c")
    return get_jsonparsed_data(url)

# for debugging
# get105prices("AAPL")
