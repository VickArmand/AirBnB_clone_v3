#!/usr/bin/python3
"""
register the blueprint app_views to your Flask instance app
"""
from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
import os
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(self):
    """
    declare a method to handle @app.teardown_appcontext
    that calls storage.close()
    """
    storage.close()


if __name__ == '__main__':
    h = os.getenv('HBNB_API_HOST') if os.getenv('HBNB_API_HOST') else '0.0.0.0'
    p = os.getenv('HBNB_API_PORT') if os.getenv('HBNB_API_PORT') else 5000
    app.run(host=h, port=p, threaded=True)
