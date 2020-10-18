import json
import requests

apikey = "" # INSERT API KEY HERE (FINNHUB.IO)

# parses JSON from HTTP GET request to finnhub API
def parseJSON(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
    return data

# parses JSON from HTTP GET request to finnhub API for analyst recommendation
def getDataRecommendations(url):
    data = parseJSON(url)
    totalExperts = data[0]['buy'] + data[0]['sell'] + data[0]['strongBuy'] + data[0]['strongSell'] + data[0]['hold']
    denominator = totalExperts * 2
    weightedSum = (data[0]['buy'] * 1) + (data[0]['sell'] * -1) + (data[0]['strongBuy'] * 2) + (data[0]['strongSell'] * -2)
    weightedAverage = weightedSum / denominator
    return weightedAverage

########################################################################
# CALL THE BELOW FUNCTIONS!!! #
########################################################################

# returns recommendation value
# closer to 1 means strong buy
# closer to -1 means strong sell
# clsoer to 0 means hold
def getRecommendations(ticker):
    url = ("https://finnhub.io/api/v1/stock/recommendation?symbol=" + ticker + "&token=" + apikey)
    return getDataRecommendations(url)


# FOR DEBUGGING
# print(getRecommendations("KSS"))
