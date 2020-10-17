#!/usr/bin/python3
# login_blueprint.py

import os
from flask import Blueprint, request, session, make_response, jsonify
from auth import authenticate


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Login
@login_blueprint.route('/login', methods=['POST'])
def post_login():
    if request.json:
        uid = request.json.get('userId')
        email = request.json.get('userEmail')
        if uid and email:
            #session['uid'] = uid
            #session['email'] = email
            #return jsonify({'success': True})
            response = make_response(jsonify({'success': True}), 200)
            response.set_cookie('uid', uid)
            response.set_cookie('email', email)
            return response
    return jsonify({'success': False}), 401


# Logout
@login_blueprint.route('/logout', methods=['POST'])
@authenticate
def post_logout():
    #session.clear()
    #return jsonify({'success': True})
    response = make_response(jsonify({'success': True}), 200)
    response.delete_cookie('uid')
    response.delete_cookie('email')
    return response
