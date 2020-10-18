#!/usr/bin/python3
# db_assets.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from config import DB_USERNAME, DB_PASSWORD, DB_BUNDLE_LOCATION


# Aggregates current asset data for a specific portfolio (user) into a mapping
# ignore_dates=True sets the mapping from asset to quantity
# ignore_dates=False sets the mapping from asset/date bought to quantity
def aggregate_assets(uid, ignore_dates=False):
    auth_provider = PlainTextAuthProvider(DB_USERNAME, DB_PASSWORD)
    cluster = Cluster(cloud={'secure_connect_bundle': DB_BUNDLE_LOCATION}, auth_provider=auth_provider)
    conn = cluster.connect()
    conn.execute('USE maelstrom;')

    query = '''
SELECT "label",
       "quantity",
       "bought"
  FROM "asset"
 WHERE "uid" = \'{uid}\';
'''.format(uid=uid)
    assets = conn.execute(query)
    conn.shutdown()

    portfolio = {}
    if ignore_dates:
        for label, quantity, date in assets:
            if label not in portfolio:
                portfolio[label] = 0
            portfolio[label] += quantity
    else:
        for label, quantity, date in assets:
            portfolio[(label, date)] = quantity
    return portfolio


# Get a user's total investing capital
def get_total_capital(uid):
    auth_provider = PlainTextAuthProvider(DB_USERNAME, DB_PASSWORD)
    cluster = Cluster(cloud={'secure_connect_bundle': DB_BUNDLE_LOCATION}, auth_provider=auth_provider)
    conn = cluster.connect()
    conn.execute('USE maelstrom;')

    query = '''
SELECT "capital"
  FROM "user"
 WHERE "uid" = \'{uid}\'
'''.format(uid=uid)
    capital = conn.execute(query).one()
    if capital:
        return capital[0]
    return None
