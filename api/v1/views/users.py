#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import request, abort
from models.user import User
from models import storage
import json


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    users = []
    for obj in storage.all(User).values():
        users.append(obj.to_dict())
    return jsonify(users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User using POST method
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name,
    raise a 400 error with the message Missing name
    If the dictionary doesn’t contain the key password,
    raise a 400 error with the message Missing password
    Returns the new User with the status code 201
    """
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    elif 'name' not in request_data.keys():
        abort(400, 'Missing name')
    elif 'password' not in request_data.keys():
        abort(400, 'Missing password')
    new_object = User(**request_data)
    storage.new(new_object)
    storage.save()
    return new_object.to_dict(), 201


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object
    If the user_id is not linked to any Amenity object,
    raise a 404 error
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """
    Updates a User object
    If the user_id is not linked to any User object,
    raise a 404 error
    You must use request.get_json from Flask to transform
    the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON,
    raise a 400 error with the message Not a JSON
    Update the User object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the User object with the status code 200
    """
    obj = storage.get(User, user_id)
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


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object
    If the user_id is not linked to any User object,
    raise a 404 error
    otherwise Returns an empty dictionary with the status code 200
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
