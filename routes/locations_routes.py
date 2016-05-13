from flask import Blueprint, request, jsonify

import geojson
import json
import os


locations = Blueprint('locations', 'locations', url_prefix='/locations')

@locations.route('/')
def get_locations():
    return jsonify({'locations': [json.loads(doc.content) for doc in Location.objects]})


@locations.route('/new', methods=['POST'])
def register_location():
    try:
        data = geojson.loads(request.get_data())
        loc = Location(content=geojson.dumps(data))
        loc.save()
    except e:
        return jsonify({'result': 'Error', 'error': str(e)})


    return jsonify({'result': 'Ok', 'id': str(loc.id)})


@locations.route('/<loc_id>')
def get_location(loc_id):
    element = Location.objects.get(id=loc_id)
    return jsonify(json.loads(element.content))
