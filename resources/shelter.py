from middleware import admin_check, id_check, read_token, strip_token
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
            return shelter.json().pop("password_digest")
        else:
            return "Unauthorized", 403

    def patch(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, Shelter, id) or admin_check(request):
                data = request.get_json()
                id = UUID(id)
                shelter = Shelter.by_id(id)
                if not shelter:
                    return 'Shelter Not found', 404
                for key in data.keys():
                    setattr(shelter, key, data[key])
                db.session.commit()
                return shelter.json().pop("password_digest")
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, Shelter, id) or admin_check(request):
                id = UUID(id)
                shelter = Shelter.by_id(id)
                if not shelter:
                    return 'Shelter Not found', 404
                copy = {}
                for key in shelter.json().pop("password_digest").keys():
                    copy[key] = shelter.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                    copy
                db.session.delete(shelter)
                db.session.commit()
                return 'Deletion Successful', copy
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class Allshelters(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            data = request.get_json()
            shelters = Shelter.by_proximity(
                data["proximity"], data["coordinates"])
            if shelters.length == 0:
                return "No Shelters Within Proximity Limit"
            return shelters
        else:
            return "Unauthorized", 403
