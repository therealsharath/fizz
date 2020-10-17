#!/usr/bin/python3
# intents_blueprint.py

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'util'))
from flask import Blueprint, request, jsonify
from auth import authenticate
from db_assets import aggregate_assets



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


@intents_blueprint.route('/intents/buy_asset', methods=['POST'])
@authenticate
def post_buy_asset():
    if not request.json:
        return jsonify({'success': False, 'authenticated': True}), 400

    asset = request.json.get('asset')
    uid = request.json.get('userId')
    if not asset or not uid:
        return jsonify({'success': False, 'authenticated': True}), 400

    portfolio = aggregate_assets(uid, ignore_dates=False)

    # Should I buy this asset? - Inputs: portfolio, asset
    # REPLACE THIS COMMENT WITH BOBBY'S CODE
    response = ''
    return jsonify({'success': True, 'authenticated': True, 'response': response}), 200


@intents_blueprint.route('/intents/sell_asset', methods=['POST'])
@authenticate
def post_sell_asset():
    if not request.json:
        return jsonify({'success': False, 'authenticated': True}), 400

    asset = request.json.get('asset')
    uid = request.json.get('userId')
    if not asset or not uid:
        return jsonify({'success': False, 'authenticated': True}), 400

    portfolio = aggregate_assets(uid, ignore_dates=False)

    # Should I sell this asset? - Inputs: portfolio, asset
    # REPLACE THIS COMMENT WITH BOBBY'S CODE
    response = ''
    return jsonify({'success': True, 'authenticated': True, 'response': response}), 200


@intents_blueprint.route('/intents/analyze_portfolio', methods=['POST'])
@authenticate
def post_analyze_portfolio():
    if not request.json:
        return jsonify({'success': False, 'authenticated': True}), 400

    uid = request.json.get('userId')
    if not uid:
        return jsonify({'success': False, 'authenticated': False}), 400

    portfolio = aggregate_assets(uid, ignore_dates=False)

    # Analyze my portfolio - Inputs: portfolio
    # REPLACE THIS COMMENT WITH BOBBY'S CODE
    response = ''
    return jsonify({'success': True, 'authenticated': True, 'response': response}), 200
