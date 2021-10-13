from middleware import read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models.shelter import Shelter
from flask import request
from models.db import db
from uuid import UUID


class ShelterById(Resource):
    def get(self, id):
        data = request.get_json()
        token = strip_token(data)
        if read_token(token)['data']:
            id = UUID(id)
            shelter = Shelter.by_id(id)
            return shelter.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            id = UUID(id)
            shelter = Shelter.by_id(id)
            for key in data.keys():
                setattr(shelter, key, data[key])
            db.session.commit()
            return shelter.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            shelter = Shelter.by_id(id)
            if not shelter:
                return {'msg': 'shelter Not found'}, 404
            copy = {}
            for key in shelter.json().keys():
                copy[key] = shelter.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(shelter)
            db.session.commit()
            return {'msg': 'shelter Deletion Successful', 'shelter': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class Allshelters(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json
            shelters = Shelter.by_proximity(
                data["proximity"], data["coordinates"])
            return shelters
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
