#!/usr/bin/python3
# login_blueprint.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'util'))
from datetime import datetime
from flask import Blueprint, request, jsonify
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from auth import authenticate
from StockPrices import getDatePrice
from config import DB_USERNAME, DB_PASSWORD, DB_BUNDLE_LOCATION


login_blueprint = Blueprint('login_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Login
@login_blueprint.route('/login', methods=['POST'])
def post_login():
    uid = request.get_json(force=True).get('userId')
    email = request.get_json(force=True).get('userEmail')

    auth_provider = PlainTextAuthProvider(DB_USERNAME, DB_PASSWORD)
    cluster = Cluster(cloud={'secure_connect_bundle': DB_BUNDLE_LOCATION}, auth_provider=auth_provider)
    conn = cluster.connect()
    conn.execute('USE maelstrom;')
    user = conn.execute('SELECT "uid", "email" FROM "user" WHERE "uid" = \'{uid}\' AND "email" = \'{email}\' ALLOW FILTERING;'.format(uid=uid, email=email)).one()
    if not user:
        user_pkid = conn.execute('SELECT "id" FROM "pkid" WHERE "label" = \'user\';').one()[0]
        conn.execute('UPDATE "pkid" SET "id" = "id" + 1 WHERE "label" = \'user\';')
        conn.execute('INSERT INTO "user" ("id", "uid", "email", "capital") VALUES ({user_pkid}, \'{uid}\', \'{email}\', {capital});'.format(user_pkid=user_pkid, uid=uid, email=email, capital=500000))
    conn.shutdown()
    return jsonify({'success': True, 'authenticated': True}), 200


# Upload portfolio
@login_blueprint.route('/portfolio/upload', methods=['POST'])
def post_portfolio_upload():
    uid = request.get_json(force=True).get('userId')
    portfolio = request.get_json(force=True).get('portfolio')

    auth_provider = PlainTextAuthProvider(DB_USERNAME, DB_PASSWORD)
    cluster = Cluster(cloud={'secure_connect_bundle': DB_BUNDLE_LOCATION}, auth_provider=auth_provider)
    conn = cluster.connect()
    conn.execute('USE maelstrom;')
    conn.execute('DELETE FROM "asset" WHERE "uid" = \'{uid}\';'.format(uid=uid))

    id = conn.execute('SELECT "id" FROM "pkid" WHERE "label" = \'asset\';').one()[0]
    c = 0
    query = 'INSERT INTO "asset" ("id", "uid", "label", "quantity", "bought", "price", "slp") VALUES '
    for asset in portfolio:
        date = datetime.strptime(asset['date'][:15], '%a %b %d %Y').strftime('%Y-%m-%d')
        price = getDatePrice(asset['ticker'], date)
        query += '({id}, \'{uid}\', \'{label}\', {quantity}, \'{bought}\', {price}, {slp}), '.format(id=id + c, uid=uid, label=asset['ticker'], quantity=asset['quantity'], bought=date, price=price, slp=asset['slp'])
        c += 1
    query = query[:-2] + ';'
    conn.execute(query)
    conn.execute('UPDATE "pkid" SET "id" = "id" + {c} WHERE "label" = \'asset\';'.format(c=c))
    conn.shutdown()
    return jsonify({'success': True, 'authenticate': True}), 200