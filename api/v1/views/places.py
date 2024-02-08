#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import request, abort
from models.place import Place
from models.city import City
from models.user import User
from models import storage
import json


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_of_a_city(city_id):
    """
    Retrieves the list of all Place objects of a City
    If the city_id is not linked to any City object,
    raise a 404 error
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = []
    for obj in city.places:
        places.append(obj.to_dict())
    return jsonify(places)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    If the city_id is not linked to any City object,
    raise a 404 error
    If the HTTP body request is not a valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    If the dictionary doesn’t contain the key user_id,
    raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object,
    raise a 404 error
    Returns the new Place with the status code 201
    """
    request_data = request.get_json()
    city = storage.get(City, city_id)
    if not request_data:
        abort(400, 'Not a JSON')
    elif 'name' not in request_data.keys():
        abort(400, 'Missing name')
    elif 'user_id' not in request_data.keys():
        abort(400, 'Missing user_id')
    elif not city:
        abort(404)
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    new_object = Place(**request_data)
    new_object.city_id = city_id
    storage.new(new_object)
    storage.save()
    return new_object.to_dict(), 201


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object
    If the place_id is not linked to any Place object,
    raise a 404 error
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    If the place_id is not linked to any Place object,
    raise a 404 error
    You must use request.get_json from Flask to transform
    the HTTP body request to a dictionary
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, state_id, created_at and updated_at
    Returns the Place object with the status code 200
    """
    obj = storage.get(Place, place_id)
    request_data = request.get_json()
    if not type(request_data) == dict:
        abort(400, 'Not a JSON')
    elif not obj:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key in request_data.keys():
        if key not in ignore_keys:
            setattr(obj, key, request_data[key])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object
    If the place_id is not linked to any Place object,
    raise a 404 error
    otherwise Returns an empty dictionary with the status code 200
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
