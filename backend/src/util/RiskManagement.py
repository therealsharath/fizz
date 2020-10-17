# totalCapital - total amount the user has to invest
# investedCapital - amount of capital invested currently
# unusedCapital - amount of capital not invested currently (total - invested)
# portfolio - maps assets to the number bought, price when bought, stop loss value
#             or strike price of downside put, and industry

# CURRENT PROBLEM:  how to uniquely identify assets?? maybe need to use tuple of
#                   asset ID and date bought?

# finds the total invested capital from the portfolio values
def calcInvestedCapital():
    investedCapital = 0;
    for asset in portfolio:
        investedCapital += portfolio[asset][0] * portfolio[asset][1]

# for an asset in the portfolio, finds out the percentage of total capital
# being risked and returns the percent risked and if risk management was used
def percentRisk(portfolio, asset):
    amountBought = portfolio[asset][0]
    priceBought = portfolio[asset][1]
    riskManagementPrice = portfolio[asset][2]

    if riskManagementPrice == None:
        riskManagementPrice = 0
    amountRisked = (priceBought - riskManagementPrice) * amountBought
    return (amountRisked / totalCapital, riskManagementPrice > 0)

# for each asset in the portfolio, checks if the percent of total capital
# risked at most one percent. Returns a mapping from an asset to the capital
# risked and if they used risk management (stop loss or downside put)
# this should take care of one percent rule and stop-loss/downside put hedging
def onePercentRule(portfolio):
    risks = {}
    for asset in porfolio:
        risks[asset] = percentRisk(portfolio, asset)
    return risks

# what should we diversify by? by company, industry, type of asset, mutual funds?
# Maybe do all of them and take a weighted average to return a diversification
# index, which could indicate how diverse the porfolio is.
def diverse(portfolio):




################################################################################
# Should I sell?

# Calculates the 5-day moving average. Need the asset price data for the past
# five days
def fiveMovingAverage(prices):
    return sum(prices) / 5

# Calculates the 20-day moving average. Need the asset price data for the past
# twenty days
def twentyMovingAverage(prices):
    return sum(prices) / 20

# Calculates if a golden cross happens between the current date and the past date.
# Needs prices data for past (20 + difference between two dates) days.
# Note that current date is at index 0, and pastDate should be > 0
def goldenCross(prices, pastDate):
    currFiveDay = fiveMovingAverage(prices[:5])
    currTwentyDay = twentyMovingAverage(prices[:20])
    currOver = currFiveDay >= currTwentyDay

    pastFiveDay = fiveMovingAverage(prices[pastDate:pastDate+5])
    pastTwentyDay = twentyMovingAverage(prices[pastDate:pastDate+20])
    pastUnder = pastFiveDay < pastTwentyDay

    return currOver and pastUnder

# Calculates if there has been a golden cross (short term MA goes above long term)
# in the past 5 days
# Needs price data for the past 25 days. Assume prices[0] is current day.
def recentGoldenCross(prices):
    for i in range(5):
