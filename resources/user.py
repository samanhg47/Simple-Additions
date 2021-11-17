from middleware import check_admin, id_check
from flask_restful import Resource
from datetime import datetime
from models.user import User
from flask import request
from models.db import db
from uuid import UUID


class AllUsers(Resource):
    def get(self):
        users = [user.json() for user in User.find_all()]
        return len(users)


class Users(Resource):
    def get(self, id):
        id = UUID(id)
        user = User.by_id(id)
        if not user:
            return 'User Not found', 404
        user = user.json()
        if check_admin(request):
            return user
        del user["password_digest"]
        if id_check(request, User, id):
            return user
        del user["email"]
        return user

    def patch(self, id):
        if id_check(request, User, id) or check_admin(request):
            id = UUID(id)
            data = request.get_json()
            user = User.by_id(id)
            if not user:
                return 'User Not found', 404
            for key in data.keys():
                setattr(user, key, data[key])
            db.session.commit()
            user = user.json()
            if check_admin(request):
                return user
            del user["password_digest"]
            return user
        else:
            return "Unauthorized", 403

    def delete(self, id):
        if id_check(request, User, id) or check_admin(request):
            id = UUID(id)
            user = User.by_id(id)
            if not user:
                return 'User Not found', 404
            copy = {}
            for key in user.json().keys():
                copy[key] = user.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(user)
            db.session.commit()
            if check_admin(request):
                return 'Deletion Successful', copy
            del copy["password_digest"]
            return 'Deletion Successful', copy
        else:
            return "Unauthorized", 403
