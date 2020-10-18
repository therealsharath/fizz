#!/usr/bin/python3
# intents_blueprint.py

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'util'))
from flask import Blueprint, request, jsonify
from db_assets import aggregate_assets, get_total_capital
from RiskManagement import shouldBuy, shouldSell, analyzePortfolio


dialogflow_blueprint = Blueprint('dialogflow_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Dialogflow intent webhook
@dialogflow_blueprint.route('/dialogflow/intent', methods=['POST'])
def post_dialogflow_webhook():
    try:
        if not request.get_json(force=True).get('queryResult').get('allRequiredParamsPresent'):
            raise TypeError
        action = request.get_json(force=True).get('queryResult').get('action')
        parameters = request.get_json(force=True).get('queryResult').get('parameters')
    except TypeError:
        return jsonify({'success': False, 'fulfillmentText': 'Something went wrong with your request.'}), 400
    chatbot_response = intents[action](**parameters)
    return jsonify({'success': True, 'fulfillmentText': chatbot_response})


# Dialogflow intent descriptions
@dialogflow_blueprint.route('/dialogflow/intents', methods=['GET'])
def get_all_intents():
    return jsonify({
        'BUY': 'Should I buy this asset?',
        'SELL': 'Should I sell this asset?',
        'ANALYZE_PORTFOLIO': 'Can you analyze my current portfolio?'
    }), 200


# Intent functions
def buy_asset(uid=None, asset=None, quantity=None, risk_management_price=None, **kwargs):
    total_capital = get_total_capital(uid)

    # Should I buy this asset? - Inputs: asset, quantity, risk price (stop loss)
    return shouldBuy(asset, quantity, risk_management_price, total_capital)


def sell_asset(asset=None, **kwargs):
    # Should I sell this asset? - Inputs: asset
    return shouldSell(asset)


def analyze_portfolio(uid=None, **kwargs):
    total_capital = get_total_capital(uid)
    portfolio = aggregate_assets(uid, ignore_dates=False)

    # Analyze my portfolio - Inputs: portfolio
    return analyzePortfolio(portfolio, total_capital)


# Dialogflow intents
intents = {
    'BUY_ASSET': buy_asset,
    'SELL_ASSET': sell_asset,
    'ANALYZE_PORTFOLIO': analyze_portfolio
}