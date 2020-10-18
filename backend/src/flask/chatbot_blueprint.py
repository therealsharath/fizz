#!/usr/bin/python3
# chatbot_blueprint.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dialogflow
from flask import Blueprint, request, jsonify
from google.api_core.exceptions import InvalidArgument
from auth import authenticate
from config import DIALOGFLOW_PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS


chatbot_blueprint = Blueprint('chatbot_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Chatbot endpoint
@chatbot_blueprint.route('/chatbot/query', methods=['POST'])
@authenticate
def post_chatbot_query():
    uid = request.get_json(force=True).get('userId')
    query = request.get_json(force=True).get('query')
    if not uid or not query:
        return jsonify({'success': False, 'authenticated': True}), 400

    DIALOGFLOW_LANGUAGE_CODE = 'en-US'
    SESSION_ID = uid

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=query, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    return jsonify({'success': True, 'authenticated': True, 'response': response.query_result.fulfillment_text})
