#!/usr/bin/python3
# intents_blueprint.py

import os
from flask import Blueprint, request, jsonify
from auth import authenticate


intents_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Dialogflow Intentions
@intents_blueprint.route('/intents/', methods=['GET'])
def get_all_intents():
    return jsonify({
        'buy_asset': 'Should I buy this asset?',
        'sell_asset': 'Should I sell this asset?',
        'analyze_portfolio': 'Can you analyze my current portfolio?',
        #'buy_any_asset': 'Which asset should I buy?',
        #'sell_any_asset': 'Which asset should I sell?'
    }), 200


@intents_blueprint.route('/intents/buy_asset')
@authenticate
def post_buy_asset():
    uid = request.json.get('userId')
