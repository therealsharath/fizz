#!/usr/bin/python3
# auth.py

import os
from flask import request, session, jsonify
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authenticate user
        #if 'uid' not in session or 'email' not in session:
        if 'uid' not in request.cookies or 'email' not in request.cookies:
            return jsonify({'success': False})
        return func(*args, **kwargs)
    return wrapper
