#!/usr/bin/python3
# api.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import IP, PORT
from login_blueprint import login_blueprint
from chatbot_blueprint import chatbot_blueprint
from dialogflow_blueprint import dialogflow_blueprint
from errors_blueprint import errors_blueprint, error_404


app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))
app.register_blueprint(login_blueprint)
app.register_blueprint(chatbot_blueprint)
app.register_blueprint(dialogflow_blueprint)
app.register_blueprint(errors_blueprint)
CORS(app)


# Fix blueprint 404 HTTP error handler with override
@app.errorhandler(404)
def error_404_override(e):
    return error_404(e)


# Home
@app.route('/', methods=['GET'])
def get_home():
    return 'Welcome to Team Maelstrom\'s HackGT 7 Project!', 200


# DialogFlow Endpoints
@app.route('/dialogflow', methods=['POST'])
def post_dialogflow():
    if request.json:
        request.json.get('queryResult')
        return jsonify({'fulfillmentText': 'This is a response from Flask!'}), 200
    return jsonify({'success': False}), 400


if __name__ == '__main__':
    app.run(IP, PORT)
