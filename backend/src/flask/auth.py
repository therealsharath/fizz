#!/usr/bin/python3
# auth.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import MySQLdb
from functools import wraps
from flask import request, jsonify
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Authenticate user
        if request.json:
            uid = request.json.get('userId')
            email = request.json.get('userEmail')

            conn = MySQLdb.connect(
                host=DB_HOST,
                user=DB_USERNAME,
                passwd=DB_PASSWORD,
                db=DB_NAME
            )
            cursor = conn.cursor()
            user = cursor.execute('''
SELECT uid,
       email
  FROM user
 WHERE uid = \'{uid}\'
   AND email = \'{email}\';'''.format(uid=uid, email=email))
            cursor.close()
            conn.close()
            if user > 0:
                return func(*args, **kwargs)
        return jsonify({'success': False, 'authenticated': False}), 401
    return wrapper
