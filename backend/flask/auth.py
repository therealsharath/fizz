#!/usr/bin/python3
# auth.py

import os
from flask import request, jsonify
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authenticate user
        if request.json:
            uid = request.json.get('uid')
            email = request.json.get('email')
            return func(*args, **kwargs)
        return jsonify({'success': False})
    return wrapper
