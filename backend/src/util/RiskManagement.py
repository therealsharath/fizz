#!/usr/bin/python3
# RiskManagement.py

from StockPrices import get105prices


# totalCapital - total amount the user has to invest
# investedCapital - amount of capital invested currently
# unusedCapital - amount of capital not invested currently (total - invested)
# portfolio - maps asset, date bought pairs to the number bought, price when bought, stop loss value
#             or strike price of downside put, and industry
# portfolio example: portfolio[(asset, date)] = (number bought, price when bought, lowest loss price, industry)

# finds the total invested capital from the portfolio values
# assetID parameter here is an asset name, date bought tuple
def calcInvestedCapital(portfolio):
    investedCapital = 0
    for assetID in portfolio:
        investedCapital += portfolio[assetID][0] * portfolio[assetID][1]
    return investedCapital

# for an asset in the portfolio, finds out the percentage of total capital
# being risked and returns the percent risked and if risk management was used
# assetID parameter here is an asset name, date bought tuple
def percentRisk(amountBought, priceBought, riskManagementPrice, totalCapital):
    if not riskManagementPrice:
        riskManagementPrice = 0
    amountRisked = (priceBought - riskManagementPrice) * amountBought
    return (amountRisked / totalCapital, riskManagementPrice > 0)

# for each asset in the portfolio, checks if the percent of total capital
# risked at most one percent. Returns a mapping from an asset to the capital
# risked and if they used risk management (stop loss or downside put)
# this should take care of one percent rule and stop-loss/downside put hedging
# assetID parameter here is an asset name, date bought tuple
def onePercentRule(portfolio, totalCapital):
    risks = {}
    for assetID in portfolio:
        assetDetails = portfolio[assetID]
        risks[assetID] = percentRisk(assetDetails[0], assetDetails[1], assetDetails[2], totalCapital)
    return risks

# what should we diversify by? by company, industry, type of asset, mutual funds?
# Maybe do all of them and take a weighted average to return a diversification
# index, which could indicate how diverse the portfolio is.
def diverse(portfolio):
    pass


################################################################################
# Calculate moving averages and crossings

# Calculates the 20-day moving average. Need the asset price data for the past
# twenty days
def twentyMovingAverage(prices):
    return sum(prices) / 20

# Calculates the 100-day moving average. Need the asset price data for the past
# hundred days
def hundredMovingAverage(prices):
    return sum(prices) / 100

# Calculates if there has been a golden cross (short term MA goes above long term)
# in the past 5 days. If there has been a golden cross, maybe we should buy.
# Needs price data for the past 105 days. Assume prices[0] is current day.
def recentGoldenCross(prices):
    currTwentyDay = twentyMovingAverage(prices[:20])
    currHundredDay = hundredMovingAverage(prices[:100])
    currOver = currTwentyDay >= currHundredDay

    pastTwentyDay = twentyMovingAverage(prices[5:25])
    pastHundredDay = hundredMovingAverage(prices[5:105])
    pastUnder = pastTwentyDay < pastHundredDay

    return currOver and pastUnder

# Calculates if there has been a death cross (short term MA goes below long term)
# in the past 5 days. If there has been a death cross, maybe we should sell.
# Needs price data for the past 105 days. Assume prices[0] is current day.
def recentDeathCross(prices):
    currTwentyDay = twentyMovingAverage(prices[:20])
    currHundredDay = hundredMovingAverage(prices[:100])
    currUnder = currTwentyDay < currHundredDay

    pastTwentyDay = twentyMovingAverage(prices[5:25])
    pastHundredDay = hundredMovingAverage(prices[5:105])
    pastOver = pastTwentyDay >= pastHundredDay

    return currUnder and pastOver



################################################################################
# Endpoints: Should I sell? Or Should I buy? Analyze my portfolio.

# takes in the user's inputs on the chatbot as well as the user's portfolio to understand if
# sell the particular asset is a good idea
def shouldSell(asset):
    prices = get105prices(asset)
    death = recentDeathCross(prices)
    # diversify???

    if death:
        return "This sounds like a good choice to sell, since the asset seems to have taken a downward trend."
    else:
        return "There is not enough information to know whether or not to sell right now."

# takes in the user's inputs on the chatbot as well as the user's total capital to understand if
# buying the particular asset is a good idea
def shouldBuy(asset, amountBought, riskManagementPrice, totalCapital):
    prices = get105prices(asset)
    gold = recentGoldenCross(prices)

    capitalRisked, riskManaged = percentRisk(amountBought, prices[0], riskManagementPrice, totalCapital)

    if gold and capitalRisked <= 0.01 and riskManaged:
        return "This sounds like a great choice to buy. Good job on managing your risks as well!"
    elif gold and capitalRisked <= 0.01 and not riskManaged:
        return "This sounds like a great choice to buy. Consider using a hedging your position through \
                downside puts or stop-loss points."
    elif gold and capitalRisked > 0.01 and riskManaged:
        return "This sounds like a great choice to buy. However, note that you are risking more capital than advisable."
    elif gold and capitalRisked > 0.01 and not riskManaged:
        return "This sounds like a great choice to buy. However, note that you are risking more capital than advisable. \
                If you hedge your position through downside puts or stop-loss points, you can lower the capital that you risk."
    elif not gold and capitalRisked <= 0.01 and riskManaged:
        return "This may not be a good choice to buy. However, you have managed your risks well. Please do more research \
                to figure out if buying this asset is worth it."
    else:
        return "This may not be a good choice to buy."

# Helper method for anaylzePortfolio that populates the string with all of the risky assets included
# in the given list and returns the populated string
def populateStringWithRisks(string, riskyAssets):
    for assetDetails in riskyAssets:
        assetName = assetDetails[0]
        capitalRisked = assetDetails[1]
        riskManaged = assetDetails[2]

        if capitalRisked > 0.01 and riskManaged:
            string += "You have done a good job hedging your position on {name}. However, note that you are risking {risked} \
                       percent of your capital, which is more than advisable.\n".format(name = assetName, risked = capitalRisked * 100)
        elif capitalRisked <= 0.01 and not riskManaged:
            string += "Good job not risking too much of your capital on {name}. However, consider using a hedging your \
                position through downside puts or stop-loss points.\n".format(name = assetName)
        elif capitalRisked > 0.01 and not riskManaged:
            string += "You are risking {risked} percent of your capital on {name}, which is more than advisable. \
                       If you hedge your position through downside puts or stop-loss points, you can lower the capital \
                       that you risk.\n".format(risked = capitalRisked * 100, name = assetName)
    return string

# analyzes the given portfolio with unused capital and some (2 or 3) of the five basic rules of risk management
def analyzePortfolio(portfolio, totalCapital):
    investedCapital = calcInvestedCapital(portfolio)
    unusedCapital = totalCapital - investedCapital

    riskyAssets = []
    risks = onePercentRule(portfolio, totalCapital)
    for assetID in keyset(risks):
        capitalRisked, riskManaged = risks[assetID]
        if capitalRisked > 0.01 or not riskManaged:
            riskyAssets.append(assetID[0], capitalRisked, riskManaged)

    if unusedCapital > 0:
        returnString = "Looks like you have some capital that you aren't using. Ask me about buying certain stocks.\n"
    else:
        returnString = "Good job utilizing all of your capital!\n"

    if len(riskyAssets) == 0:
        returnString += "It also looks like you have mitigated much of your risks. Great job!"
    else:
        returnString = populateStringWithRisks(returnString, riskyAssets)

    return returnString
