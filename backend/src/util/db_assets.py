#!/usr/bin/python3
# db_assets.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import MySQLdb
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME


# Aggregates current asset data for a specific portfolio (user) into a mapping
# ignore_dates=True sets the mapping from asset to quantity
# ignore_dates=False sets the mapping from asset/date bought to quantity
def aggregate_assets(uid, ignore_dates=False):
    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )
    cursor = conn.cursor()

    cursor.execute('''
SELECT label,
       quantity,
       bought,
       price,
       slp
  FROM asset
 WHERE uid = \'{uid}\';'''.format(uid=uid))
    assets = cursor.fetchall()
    cursor.close()
    conn.close()

    portfolio = {}
    if ignore_dates:
        for label, quantity, date in assets:
            if label not in portfolio:
                portfolio[label] = 0
            portfolio[label] += quantity
    else:
        for label, quantity, date, price, slp in assets:
            portfolio[(label, date)] = (quantity, price, slp)
    return portfolio


# Get a user's total investing capital
def get_total_capital(uid):
    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute('''
SELECT capital
  FROM user
 WHERE uid = \'{uid}\';'''.format(uid=uid))
    capital = cursor.fetchone()
    cursor.close()
    conn.close()
    if capital:
        return capital
    return None
