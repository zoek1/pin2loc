from flask import Blueprint, request, jsonify, Response

import geojson
import json
import os


locations = Blueprint('locations', 'locations', url_prefix='/locations')

@locations.route('/')
def get_locations():
    locations = []

    for location_object in Location.objects:
        json_object = json.loads(location_object.content)

        if not 'properties' in json_object:
            json_object['properties'] = {}

        json_object['properties']['id'] = str(location_object.id)
        locations.append(json_object)

    return Response(json.dumps(locations), mimetype='text/json')


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
