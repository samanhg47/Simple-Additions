from middleware import check_admin, id_check
from flask_restful import Resource
from models.shelter import Shelter
from datetime import datetime
from flask import request
from models.db import db


class Shelters(Resource):
    def get(self, id):
        shelter = Shelter.by_id(id)
        if shelter:
            shelter = shelter.json()
            return shelter
        else:
            return 'Shelter Not found', 404

    def patch(self, id):
        if id_check(request, Shelter, id) or check_admin(request):
            data = request.get_json()
            shelter = Shelter.by_id(id)
            if shelter:
                for key in data.keys():
                    setattr(shelter, key, data[key])
                db.session.commit()
                shelter = shelter.json()
                if check_admin(request):
                    return shelter
                return shelter
            else:
                return 'Shelter Not found', 404
        else:
            return "Unauthorized", 403

    def delete(self, id):
        if id_check(request, Shelter, id) or check_admin(request):
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
                return {'Deletion Successful': copy}
            else:
                return 'Shelter Not found', 404
        else:
            return "Unauthorized", 401


class By_Proximity(Resource):
    def post(self):
        print()
        print()
        print("4")
        print()
        print()
        data = request.get_json()
        print()
        print()
        print(data)
        print()
        print()
        shelters = Shelter.by_proximity(
            data["coordinates"], data["proximity"]
        )

        if type(shelters) is list and len(shelters) == 0:
            return "No Shelters Within Proximity Limit", 404
        return shelters
