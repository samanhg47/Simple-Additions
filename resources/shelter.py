import re
from middleware import id_check, read_token, strip_admin, strip_token
from flask_restful import Resource
from models.shelter import Shelter
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID


class Shelters(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token):
            id = UUID(id)
            shelter = Shelter.by_id(id)
            if not shelter:
                return 'Shelter Not found', 404
            shelter = shelter.json()
            if read_token(strip_admin(request)):
                return shelter
            del shelter["password_digest"]
            return shelter
        else:
            return "Unauthorized", 403

    def patch(self, id):
        if read_token(strip_token(request)):
            if id_check(request, Shelter, id) or read_token(strip_admin(request)):
                data = request.get_json()
                id = UUID(id)
                shelter = Shelter.by_id(id)
                if not shelter:
                    return 'Shelter Not found', 404
                for key in data.keys():
                    setattr(shelter, key, data[key])
                db.session.commit()
                shelter = shelter.json()
                if read_token(strip_admin(request)):
                    return shelter
                del shelter["password_digest"]
                return shelter
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, Shelter, id) or read_token(strip_admin(request)):
                id = UUID(id)
                shelter = Shelter.by_id(id)
                if not shelter:
                    return 'Shelter Not found', 404
                copy = {}
                for key in shelter.json().keys():
                    copy[key] = shelter.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(shelter)
                db.session.commit()
                if read_token(strip_admin(request)):
                    return {'Deletion Successful': copy}
                del copy["password_digest"]
                return {'Deletion Successful': copy}
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class Allshelters(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):

            data = request.get_json()
            if "proximity" not in data.keys():
                return "Proximity Not Provided", 400
            if "coordinates" not in data.keys():
                return "Coordinates Not Provided", 400
            shelters = Shelter.by_proximity(
                data["coordinates"], data["proximity"])
            if len(shelters) == 0:
                return "No Shelters Within Proximity Limit"
            if read_token(strip_admin(request)):
                return shelters
            for shelter in shelters:
                del shelter["password_digest"]
            return shelters
        else:
            return "Unauthorized", 403
