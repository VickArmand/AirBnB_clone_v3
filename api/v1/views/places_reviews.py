#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import request, abort
from models.state import State
from models.city import City
from models import storage
import json


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_of_a_state(state_id):
    """
    Retrieves the list of all City objects of a State
    If the state_id is not linked to any State object,
    raise a 404 error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for obj in state.cities:
        cities.append(obj.to_dict())
    return jsonify(cities)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    If the state_id is not linked to any State object,
    raise a 404 error
    If the HTTP body request is not a valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new City with the status code 201
    """
    request_data = request.get_json()
    state = storage.get(State, state_id)
    if not request_data:
        abort(400, 'Not a JSON')
    elif 'name' not in request_data.keys():
        abort(400, 'Missing name')
    elif not state:
        abort(404)
    print('name' in request_data.keys())
    new_object = City(**request_data)
    new_object.state_id = state_id
    storage.new(new_object)
    storage.save()
    return new_object.to_dict(), 201


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    If the city_id is not linked to any city object,
    raise a 404 error
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    Updates a City object: PUT /api/v1/cities/<city_id>
    If the city_id is not linked to any City object,
    raise a 404 error
    You must use request.get_json from Flask to transform
    the HTTP body request to a dictionary
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the City object with all key-value pairs of the dictionary
    Ignore keys: id, state_id, created_at and updated_at
    Returns the City object with the status code 200
    """
    obj = storage.get(City, city_id)
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


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    If the city_id is not linked to any City object,
    raise a 404 error
    otherwise Returns an empty dictionary with the status code 200
    """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
