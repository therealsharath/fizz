#!/usr/bin/python3
# login_blueprint.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'util'))
import MySQLdb
from datetime import datetime
from flask import Blueprint, request, jsonify
from auth import authenticate
from StockPrices import getDatePrice
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Login
@login_blueprint.route('/login', methods=['POST'])
def post_login():
    uid = request.get_json(force=True).get('userId')
    email = request.get_json(force=True).get('userEmail')

    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )
    cursor = conn.cursor()
    if cursor.execute('''
SELECT uid,
       email
  FROM user
 WHERE uid = \'{uid}\'
   AND email = \'{email}\';'''.format(uid=uid, email=email)) == 0:
        cursor.execute('''
INSERT INTO user
            (
                uid,
                email
            )
     VALUES (
                \'{uid}\',
                \'{email}\'
            );
'''.format(uid=uid, email=email))
        conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'authenticated': True}), 200


# Upload portfolio
@login_blueprint.route('/portfolio/upload', methods=['POST'])
@authenticate
def post_portfolio_upload():
    uid = request.get_json(force=True).get('userId')
    portfolio = request.get_json(force=True).get('portfolio')

    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )
    cursor = conn.cursor()

    cursor.execute('''
DELETE FROM asset
      WHERE uid = \'{uid}\';
'''.format(uid=uid))

    query = '''
INSERT INTO asset
            (
                uid,
                label,
                quantity,
                bought,
                price,
                slp
            )
     VALUES '''

    for asset in portfolio:
        date = datetime.strptime(asset['date'][:15], '%a %b %d %Y').strftime('%Y-%m-%d')
        price = getDatePrice(asset['ticker'], date)
        query += '(\'{uid}\', \'{label}\', {quantity}, \'{bought}\', {price}, {slp}), '.format(uid=uid, label=asset['ticker'].upper(), quantity=asset['quantity'], bought=date, price=price, slp=asset['slp'])
    query = query[:-2] + ';'
    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({'success': True, 'authenticate': True}), 200
