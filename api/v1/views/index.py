#!/usr/bin/python3
"""creates routes using blueprints"""
from api.v1.views import app_views
import json


@app_views.route('/status')
def ok():
    """
    create a route /status on the object app_views that
    returns a JSON: "status": "OK
    """
    return json.dumps({
        'status': 'OK'
        })
