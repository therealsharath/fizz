#!/usr/bin/python3
# auth.py

import os
from flask import session, jsonify
from functools import wraps


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authenticate user
        if 'uid' in session and 'password' in session:
            return func(*args, **kwargs)
        return jsonify({'success': False})
    return wrapper
