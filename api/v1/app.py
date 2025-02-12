#!/usr/bin/python3
"""
register the blueprint app_views
to your Flask instance app
"""
import os
from flask import Flask, render_template, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown(self):
    """closes the current db session after execution"""
    storage.close()


@app.errorhandler(404)
def error_404(err):
    """
    a handler for 404 errors that returns a JSON-formatted
    404 status code response.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    h = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') else '0.0.0.0'
    p = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') else 5000
    app.run(host=h, port=p, threaded=True)
