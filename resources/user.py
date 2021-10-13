from middleware import read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models.user import User
from flask import request
from models.db import db


class Users(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            user = User.by_id(id)
            return user.json().pop("password_digest")
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            user = User.by_id(id)
            for key in data.keys():
                setattr(user, key, data[key])
            db.session.commit()
            return user.json().pop("password_digest")
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            user = User.by_id(id)
            if not user:
                return {'msg': 'User Not found'}, 404
            copy = {}
            for key in user.json().pop("password_digest").keys():
                copy[key] = user.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(user)
            db.session.commit()
            return {'Deletion Successful', copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class AllUsers(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            users = User.find_all()
            return [user.json().pop("password_digest") for user in users]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
