#!/usr/bin/python3
# login_blueprint.py

import os
from flask import Blueprint, request, jsonify
from auth import authenticate


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Login
@login_blueprint.route('/login', methods=['POST'])
@authenticate
def post_login():
    return jsonify({'success': True, 'authenticated': True}), 200
