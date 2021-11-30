import re
from middleware import check_admin, id_check
from flask_restful import Resource
from models.shelter import Shelter
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID


class Shelters(Resource):
    def get(self, id):
        id = UUID(id)
        shelter = Shelter.by_id(id)
        if shelter:
            shelter = shelter.json()
            del shelter["password_digest"]
            return shelter
        else:
            return 'Shelter Not found', 404

    def patch(self, id):
        if id_check(request, Shelter, id) or check_admin(request):
            data = request.get_json()
            id = UUID(id)
            shelter = Shelter.by_id(id)
            if shelter:
                for key in data.keys():
                    setattr(shelter, key, data[key])
                db.session.commit()
                shelter = shelter.json()
                if check_admin(request):
                    return shelter
                del shelter["password_digest"]
                return shelter
            else:
                return 'Shelter Not found', 404
        else:
            return "Unauthorized", 403

    def delete(self, id):
        if id_check(request, Shelter, id) or check_admin(request):
            id = UUID(id)
            shelter = Shelter.by_id(id)
            if shelter:
                copy = {}
                for key in shelter.json().keys():
                    copy[key] = shelter.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(shelter)
                db.session.commit()
                if check_admin(request):
                    return {'Deletion Successful': copy}
                del copy["password_digest"]
                return {'Deletion Successful': copy}
            else:
                return 'Shelter Not found', 404
        else:
            return "Unauthorized", 401


class By_Proximity(Resource):
    def post(self):
        data = request.get_json()
        shelters = Shelter.by_proximity(
            data["coordinates"], data["proximity"]
        )

        if len(shelters) == 0:
            return "No Shelters Within Proximity Limit", 404
        for shelter in shelters:
            del shelter["password_digest"]
        return shelters
