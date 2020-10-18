#!/usr/bin/python3
# RiskManagement.py

from StockPrices import get105prices
from AnalystRecommendations import getRecommendations


# totalCapital - total amount the user has to invest
# investedCapital - amount of capital invested currently
# unusedCapital - amount of capital not invested currently (total - invested)
# portfolio - maps asset, date bought pairs to the number bought, price when bought, stop loss value
#             or strike price of downside put, and industry
# portfolio example: portfolio[(asset, date)] = (number bought, price when bought, lowest loss price, industry)

################################################################################
# Calculate risk management basics (for portfolio analysis)

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
# Calculate moving averages and crossings (for buy/sell analysis)

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

#
def calcBuySellOpinions(buySellIndex):
    if buySellIndex < -0.6:
        return "sell, sell, sell!"
    elif buySellIndex < -0.2:
        return "sell, but maybe hold."
    elif buySellIndex < 0.2:
        return "hold."
    elif buySellIndex < 0.6:
        return "buy, but maybe hold."
    else:
        return "buy, buy, buy!"


################################################################################
# Endpoints: Should I sell? Or Should I buy? Analyze my portfolio.

# takes in the user's inputs on the chatbot as well as the user's portfolio to understand if
# sell the particular asset is a good idea
def shouldSell(asset):
    prices = get105prices(asset)
    death = recentDeathCross(prices)
    buySellIndex = getRecommendations(asset)
    recommend = calcBuySellOpinions(buySellIndex)
    # diversify???

    if death:
        if buySellIndex < -0.2:
            return "{name} sounds like a good choice to sell, since the asset seems to have taken a downward trend. \
                    Experts also say to {opinion}".format(name = asset, opinion = recommend)
        elif buySellIndex < 0.2:
            return "{name} sounds like a good choice to sell, since the asset seems to have taken a downward trend. \
                    However, experts are saying that you should \
                    {opinion}".format(name = asset, opinion = recommend)
        else:
            return "Our algorithm determines that {name} may be a good choice to sell, since the asset seems to have \
                    taken a downward trend. However, experts are saying not to sell. I advise that you do some \
                    additional research into this.".format(name = asset)
    else:
        if buySellIndex > 0.2:
            return "Taking into account our algorithm and the opinions of experts, \
                    it seems that you should not sell {name}".format(name = asset)
        elif buySellIndex > -0.2:
            return "According to our algorithm and the recommendations of experts, it seems best to \
                    {opinion}".format(opinion = recommend)
        else:
            return "Our algorithm does not see a clear reason to sell, but experts say that you should {opinion} \
                    I advise that you do some additional research.".format(opinion = recommend)

# takes in the user's inputs on the chatbot as well as the user's total capital to understand if
# buying the particular asset is a good idea
def shouldBuy(asset, amountBought, riskManagementPrice, totalCapital):
    prices = get105prices(asset)
    gold = recentGoldenCross(prices)
    buySellIndex = getRecommendations(asset)
    recommend = calcBuySellOpinions(buySellIndex)

    capitalRisked, riskManaged = percentRisk(amountBought, prices[0], riskManagementPrice, totalCapital)

    returnString = "something is wrong"

    if gold:
        returnString = "Our algorithm determined that {name} is a good choice to buy, since the asset seems to \
                        have taken an upward trend. ".format(name = asset)

        if buySellIndex < -0.2:
            returnString += "However, experts are saying not to buy {name}. So I advise that you do some \
                             more research into this.".format(name = asset)
        elif buySellIndex < 0.2:
            returnString += "Experts note that you should be more cautious, and hold."
        else:
            returnString += "Experts agree that you should {opinion}".format(opinion = recommend)

        if capitalRisked <= 0.01 and riskManaged:
            returnString += " Good job on managing your risks as well!"
        if capitalRisked <= 0.01 and not riskManaged:
            returnString += " Consider hedging your position through downside puts or stop-loss points."
        if capitalRisked > 0.01 and riskManaged:
            returnString += " Note that you are risking {risked} percent of your capital, which is more than \
                             advisable.".format(risked = capitalRisked * 100)
        if capitalRisked > 0.01 and not riskManaged:
            returnString += " However, you are risking {risked} percent of your capital, which is more than advisable. \
                             If you hedge your position through downside puts or stop-loss points, you can lower the \
                             capital that you risk.".format(risked = capitalRisked * 100)
    else:
        if buySellIndex > 0.2:
            returnString =  "Our algorithm does not see a clear reason to buy, but experts say that you should {opinion} \
                             I advise that you do some additional research.".format(opinion = recommend)
        else:
            returnString = "Taking into account our algorithm and the recommendations of experts, we would advise \
                            you not to buy {name}".format(name = asset)

        if capitalRisked <= 0.01 and riskManaged:
            returnString += " Regardless, good job on managing your risks as well!"
        if capitalRisked <= 0.01 and not riskManaged:
            returnString += " Regardless, consider hedging your position through downside puts or stop-loss points."
        if capitalRisked > 0.01 and riskManaged:
            returnString += " However, note that you are risking {risked} percent of your capital, which is more than \
                             advisable.".format(risked = capitalRisked * 100)
        if capitalRisked > 0.01 and not riskManaged:
            returnString += " However, you are risking {risked} percent of your capital, which is more than advisable. \
                             If you hedge your position through downside puts or stop-loss points, you can lower the \
                             capital that you risk.".format(risked = capitalRisked * 100)
    return returnString

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
