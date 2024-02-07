#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import request, abort
from models.state import State
from models import storage
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    states = []
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """
    Creates a State using POST method
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    Returns the new State with the status code 201
    """
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    elif 'name' not in request_data.keys():
        abort(400, 'Missing name')
    new_object = State(**request_data)
    storage.new(new_object)
    storage.save()
    return new_object.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object
    If the state_id is not linked to any State object,
    raise a 404 error
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State object
    If the state_id is not linked to any State object, raise a 404 error
    You must use request.get_json from Flask to transform
    the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the State object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the State object with the status code 200
    """
    obj = storage.get(State, state_id)
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


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object
    If the state_id is not linked to any State object,
    raise a 404 error
    otherwise Returns an empty dictionary with the status code 200
    """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
