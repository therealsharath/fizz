#!/usr/bin/python3
# auth.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from functools import wraps
from flask import request, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import DB_USERNAME, DB_PASSWORD, DB_BUNDLE_LOCATION


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authenticate user
        if request.json:
            uid = request.json.get('uid')
            email = request.json.get('email')

            auth_provider = PlainTextAuthProvider(DB_USERNAME, DB_PASSWORD)
            cluster = Cluster(cloud={'secure_connect_bundle': DB_BUNDLE_LOCATION}, auth_provider=auth_provider)
            conn = cluster.connect()
            users = conn.execute('''
            ''')

            return func(*args, **kwargs)
        return jsonify({'success': False, 'authenticated': False}), 401
    return wrapper
