import json
import requests

# parses JSON from HTTP GET request to blackRock API
def parseJSON(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
    return data

# parses JSON from HTTP GET request to blackRock API for risk calculation
def getDataRisk(url):
    data = parseJSON(url)
    prefix = data['resultMap']['RETURNS'][0]['latestPerf']
    risk = 0
    sharpe = 0
    fullAnnualizedRisk = prefix['sinceStartDateRiskAnnualized']
    fullSharpeRatio = prefix['sinceStartDateSharpeRatio']
    oneYearAnnualizedRisk = prefix['oneYearRiskAnnualized']
    oneYearSharpeRatio = prefix['oneYearSharpeRatio']

    risk = 0.5 - (0.35 * fullAnnualizedRisk + 0.65 * oneYearAnnualizedRisk)
    sharpe = 0.35 * fullSharpeRatio + 0.65 * oneYearSharpeRatio

    return ((risk + sharpe) - 1) / 4

########################################################################
# CALL THE BELOW FUNCTIONS!!! #
########################################################################

# returns risk value from -1 to 1
# values less than 0 are deemed as "risky"
def getRisk(ticker):
    url = ("https://www.blackrock.com/tools/hackathon/performance?fullCalculation=false&identifiers=" + ticker + "&includePerformanceChart=false&includeReturnsMap=false&includeScore=true")
    return getDataRisk(url)


# FOR DEBUGGING
# print(getRisk("KSS"))
