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
from models.amenity import Amenity
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


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the
    JSON in the body of the request
    The JSON can contain 3 optional keys:
        states: list of State ids
        cities: list of City ids
        amenities: list of Amenity ids
    Search rules:
        If the HTTP request body is not valid JSON,
        raise a 400 error with the message Not a JSON
        If the JSON body is empty or each list of all keys
        are empty: retrieve all Place objects
        If states list is not empty, results should include
        all Place objects for each State id listed
        If cities list is not empty, results should include
        all Place objects for each City id listed
        Keys states and cities are inclusive.
        Search results should include all Place objects
        in storage related to each City in every State
        listed in states, plus every City listed individually
        in cities, unless that City was already included by states.
            Context:
                State A has 2 cities A1 and A2
                State B has 3 cities B1, B2 and B3
                A1 has 1 place
                A2 has 2 places
                B1 has 3 places
                B2 has 4 places
                B3 has 5 places
            Search: states = State A and cities = B2
            Result: all 4 places from the city B2 and the place
            from the city A1 and the 2 places of the city A2
            (because they are part of State A) => 7 places returned
    If amenities list is not empty, limit search results to
    only Place objects having all Amenity ids listed
    The key amenities is exclusive, acting as a filter on the
    results generated by states and cities, or on all Place
    if states and cities are both empty or missing.
    Results will only include Place objects having all listed
    amenities.
    If a Place doesn’t have even one of these amenities,
    it won’t be retrieved.
    """
    request_data = request.get_json()
    if type(request_data) != dict:
        abort(400, 'Not a JSON')
    results = []
    new_results = []
    objects = storage.all(Place)
    if not request_data:
        results = [obj.to_dict() for obj in objects.values()]
        return jsonify(results)
    empty_values = 0
    for ls in request_data.values():
        if not ls:
            empty_values += 1
    if empty_values == len(request_data):
        results = [obj.to_dict() for obj in objects.values()]
        return jsonify(results)
    optional_keys = ['states', 'cities', 'amenities']
    for key in optional_keys:
        id_list = request_data.get(key)
        if id_list and key == 'states':
            for c_id in id_list:
                results = [obj for obj in objects.values()
                           if obj.cities.state_id == c_id]
        elif id_list and key == 'cities':
            for c_id in id_list:
                results = [obj for obj in objects.values()
                           if obj.city_id == c_id]
        elif id_list and key == 'amenities':
            for c_id in id_list:
                amenity = storage.get(Amenity, c_id)
                if results:
                    new_results = [obj for obj in results
                               if amenity in obj.amenities]
                else:
                    results = [obj for obj in objects.values()
                               if amenity in obj.amenities]
            if new_results:
                results = new_results
    return jsonify([obj.to_dict() for obj in results])
