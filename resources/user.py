from middleware import read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models.user import User
from flask import request
from models.db import db
from uuid import UUID


class Users(Resource):
    def get(self, id):
        token = strip_token(data)
        if read_token(token)['data']:
            id = UUID(id)
            user = User.by_id(id)
            return user.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            id = UUID(id)
            user = User.by_id(id)
            for key in data.keys():
                setattr(user, key, data[key])
            db.session.commit()
            return user.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            user = User.by_id(id)
            if not user:
                return {'msg': 'User Not found'}, 404
            copy = {}
            for key in user.json().keys():
                copy[key] = user.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(user)
            db.session.commit()
            return {'msg': 'User Deletion Successful', 'user': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class AllUsers(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            users = User.find_all()
            return users
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
