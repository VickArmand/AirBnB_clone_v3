#!/usr/bin/python3
"""creates routes using blueprints"""
from api.v1.views import app_views
import json
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def ok():
    """
    create a route /status on the object app_views that
    returns a JSON: "status": "OK
    """
    return json.dumps({
        'status': 'OK'
        })


@app_views.route('/stats')
def count():
    keys = ["amenities", "cities", "places", "reviews", "states", "users"]
    val = [Amenity, City, Place, Review, State, User]
    resp = {}
    for index in range(len(val)):
        resp[keys[index]] = storage.count(val[index])
    return json.dumps(resp)
