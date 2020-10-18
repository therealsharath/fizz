#!/usr/bin/python3
# config.py

import os


if __name__ == '__main__':
    exit(0)


# Flask Server
IP = '0.0.0.0'  # Flask server IP address
PORT = 80  # Flask server port

# DataStax Astra
DB_USERNAME = ''  # DataStax Astra database username
DB_PASSWORD = ''  # DataStax Astra database password
DB_BUNDLE_LOCATION = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db', 'secure-connect-hackgt-7.zip')  # Path to DataStax Astra secure connect bundle zip file

# Dialogflow
DIALOGFLOW_PROJECT_ID = ''  # Project ID of Dialogflow application

# API Keys
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hackgt7-google.json')  # Location of JSON file containing Google application credentials
FMP_API_KEY = ''  # Financial Modeling Prep API Key
