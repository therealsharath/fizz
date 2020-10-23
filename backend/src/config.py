#!/usr/bin/python3
# config.py

import os


if __name__ == '__main__':
    exit(0)


# Flask Server
IP = '0.0.0.0'  # Flask server IP address
PORT = 80  # Flask server port

# MySQL Database
DB_USERNAME = ''  # MySQL database username
DB_PASSWORD = ''  # MySQL database password
DB_HOST = ''  # MySQL database hostname
DB_NAME = ''  # MySQL database name

# Dialogflow
DIALOGFLOW_PROJECT_ID = ''  # Project ID of Dialogflow application

# API Keys
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hackgt7-google.json')  # Location of JSON file containing Google application credentials
FMP_API_KEY = ''  # Financial Modeling Prep API Key
FINNHUB_API_KEY = ''  # Finnhub.io API Key
