#!/usr/bin/python3
"""
a new view for State objects that
handles all default RESTFul API actions
"""
from api.v1.app import app_views, jsonify
from flask import abort
from models.amenity import Amenity
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def amenities_of_a_place(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    If the place_id is not linked to any Place object,
    raise a 404 error
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenities = []
    for amenity in place.amenities:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_place(place_id, amenity_id):
    """
    No HTTP body needed
    If the place_id is not linked to any Place object,
    raise a 404 error
    If the amenity_id is not linked to any Amenity object,
    raise a 404 error
    If the Amenity is already linked to the Place,
    return the Amenity with the status code 200
    Returns the Amenity with the status code 201
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place and not amenity:
        abort(404)
    if amenity in place.amenities:
        return amenity.to_dict(), 200
    place.amenity_id = amenity_id
    storage.new(place)
    storage.save()
    return jsonify(amenity.to_dict()), 201



@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def unlink_amenity_place(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    If the place_id is not linked to any Place object,
    raise a 404 error
    If the amenity_id is not linked to any Amenity object,
    raise a 404 error
    If the Amenity is not linked to the Place before the request,
    raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity or amenity not in place.amenities:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200
