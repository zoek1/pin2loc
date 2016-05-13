import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'routes'))

from flask import Flask
from  flask.ext.mongoengine import MongoEngine

import location_model
import locations_routes

def create_app():

    app = Flask(__name__)

    app.config["MONGO_SETTINGS"] = {
        'db': 'pin2loc',
        'host': os.getenv('MONGODB_URI', 'localhost')
    }

    app.config["SECRET_KEY"] = os.getenv('LOCAL_KEY', "KeepThisS3cr3t")

    db = MongoEngine(app)
    Location = location_model.factory(db)

    app.register_blueprint(locations_routes.locations)
    locations_routes.Location = Location

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

