#!/usr/bin/python3
# errors_blueprint.py

import os
from flask import Blueprint, render_template


errors_blueprint = Blueprint('errors_blueprint', __name__, template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))


# Error handlers
@errors_blueprint.errorhandler(404)
def error_404(e):
    return render_template('error_templates/404.html'), 404


@errors_blueprint.errorhandler(400)
def error_400(e):
    return 'HTTP 400 - Bad Request', 400
