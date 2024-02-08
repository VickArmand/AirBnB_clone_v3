#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import request, abort
from models.review import Review
from models.place import Place
from models import storage
import json


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews_of_a_place(place_id):
    """
    Retrieves the list of all Review objects of a Place
    If the place_id is not linked to any Place object,
    raise a 404 error
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = []
    for obj in place.reviews:
        reviews.append(obj.to_dict())
    return jsonify(reviews)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """
    If the place_id is not linked to any Place object,
    raise a 404 error
    If the HTTP body request is not a valid JSON,
    raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id,
    raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object,
    raise a 404 error
    If the dictionary doesn’t contain the key text,
    raise a 400 error with the message Missing text
    Returns the new Review with the status code 201
    """
    request_data = request.get_json()
    place = storage.get(Place, place_id)
    if not request_data:
        abort(400, 'Not a JSON')
    elif 'text' not in request_data.keys():
        abort(400, 'Missing text')
    elif 'user_id' not in request_data.keys():
        abort(400, 'Missing user_id')
    elif not place:
        abort(404)
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    new_object = Review(**request_data)
    new_object.place_id = state_id
    storage.new(new_object)
    storage.save()
    return new_object.to_dict(), 201


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object
    If the review_id is not linked to any Review object,
    raise a 404 error
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    If the review_id is not linked to any Review object,
    raise a 404 error
    If the HTTP request body is not valid JSON,
    raise a 400 error with the message Not a JSON
    Ignore keys: id, user_id, place_id, created_at and updated_at
    Returns the Review object with the status code 200
    """
    obj = storage.get(Review, review_id)
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


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object
    If the review_id is not linked to any Review object,
    raise a 404 error
    otherwise Returns an empty dictionary with the status code 200
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})
