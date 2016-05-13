import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))

from flask import Flask, jsonify, request, abort

from  flask.ext.mongoengine import MongoEngine
import random
import locations
import geojson
import json

app = Flask(__name__)

app.config["MONGO_SETTINGS"] = {
    'db': 'pin2loc',
    'host': os.getenv('MONGODB_URI', 'localhost')
}

app.config["SECRET_KEY"] = os.getenv('LOCAL_KEY', "KeepThisS3cr3t")

db = MongoEngine(app)

Location = locations.factory(db)

@app.route('/locations')
def get_locations():
    return jsonify({'locations': [json.loads(doc.content) for doc in Location.objects]})

@app.route('/locations/<loc_id>')
def get_location(loc_id):
    element = Location.objects.get(id=loc_id)
    return jsonify(json.loads(element.content))

@app.route('/locations/new', methods=['POST'])
def register_location():
    try:
        data = geojson.loads(request.get_data())
        loc = Location(content=geojson.dumps(data))
        loc.save()
    except e:
        return jsonify({'result': 'Error', 'error': str(e)})


    return jsonify({'result': 'Ok', 'id': str(loc.id)})


if __name__ == "__main__":
    app.run(debug=True)

