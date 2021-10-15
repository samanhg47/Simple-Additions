from middleware import admin_check, id_check, read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models.user import User
from flask import request
from models.db import db
from uuid import UUID


class Users(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, User, id) or admin_check(request):
                id = UUID(id)
                user = User.by_id(id)
                if not user:
                    return 'User Not found', 404
                return user.json()
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def patch(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, User, id) or admin_check(request):
                id = UUID(id)
                data = request.get_json()
                user = User.by_id(id)
                if not user:
                    return 'User Not found', 404
                for key in data.keys():
                    setattr(user, key, data[key])
                db.session.commit()
                return user.json().pop("password_digest")
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, User, id) or admin_check(request):
                id = UUID(id)
                user = User.by_id(id)
                if not user:
                    return 'User Not found', 404
                copy = {}
                for key in user.json().pop("password_digest").keys():
                    copy[key] = user.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(user)
                db.session.commit()
                return 'Deletion Successful', copy
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403
