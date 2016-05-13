import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'routes'))

from flask import Flask
from  flask.ext.mongoengine import MongoEngine

import location_model
import locations_routes

def create_app():

    new_app = Flask(__name__)

    new_app.config["MONGODB_SETTINGS"] = {
        'db': 'locations',
        'host': os.getenv('MONGODB_URI', 'localhost')
    }

    new_app.config["SECRET_KEY"] = os.getenv('LOCAL_KEY', "KeepThisS3cr3t")

    db = MongoEngine(new_app)
    Location = location_model.factory(db)

    new_app.register_blueprint(locations_routes.locations)
    locations_routes.Location = Location

    return new_app


PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "False") == "True"
HOST = os.getenv("HOST", "0.0.0.0")

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, debug=DEBUG, port=PORT)
