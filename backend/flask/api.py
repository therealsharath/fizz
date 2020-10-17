#!/usr/bin/python3
# api.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask
from flask import CORS
from config import IP, PORT
from errors_blueprint import errors_blueprint, error_404


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))
app.register_blueprint(errors_blueprint)
CORS(app)


# Fix blueprint 404 HTTP error handler with override
@app.error_handler(404)
def error_404_override(e):
    return error_404(e)


# Home
@app.route('/', methods=['GET'])
def get_home():
    return 'Welcome to Team Maelstrom\'s HackGT 7 Project!', 200


if __name__ == '__main__':
    app.run(IP, PORT)