#!/usr/bin/python3
# login_blueprint.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Blueprint, request, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from auth import authenticate
from config import DB_USERNAME, DB_PASSWORD, DB_BUNDLE_LOCATION


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Login
@login_blueprint.route('/login', methods=['POST'])
@authenticate
def post_login():
    return jsonify({'success': True, 'authenticated': True}), 200


# Create user
@login_blueprint.route('/user/create', methods=['POST'])
def post_create_user():
    if not request.json:
        return jsonify({'success': False, 'authenticated': False}), 400

    uid = request.json.get('userId')
    email = request.json.get('userEmail')
    if not uid or not email:
        return jsonify({'success': False, 'authenticated': False}), 400
