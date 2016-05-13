import datetime

def factory(db):
    class Locations(db.Document):
        content = db.StringField(required=True)



    return Locations
