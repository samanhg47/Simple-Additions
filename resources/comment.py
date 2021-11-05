from middleware import strip_admin, id_check, read_token, strip_token
from resources.admin import censor_language
from flask_restful import Resource
from models.comment import Comment
from datetime import datetime
from models.user import User
from flask import request
from models.db import db
from uuid import UUID


class AllComments(Resource):
    def post(self):
        if read_token(strip_token(request))['data']:
            data = request.get_json()
            data["body"] = censor_language(data)
            comment = Comment(**data)
            comment.create()
            return comment.json(), 201
        else:
            return "Unauthorized", 403


class Comments(Resource):
    def patch(self, id):
        if read_token(strip_token(request))['data']:
            if id_check(request, Comment, id) or read_token(strip_admin(request)):
                data = request.get_json()
                id = UUID(id)
                comment = Comment.by_id(id)
                if not comment:
                    return 'Comment Not Found', 404
                data["body"] = censor_language(data)
                for key in data.keys():
                    setattr(comment, key, data[key])
                db.session.commit()
                return comment.json()
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        if read_token(strip_token(request))['data']:
            if id_check(request, Comment, id) or read_token(strip_admin(request)):
                id = UUID(id)
                comment = Comment.by_id(id)
                if not comment:
                    return 'Comment Not Found', 404
                copy = {}
                for key in comment.json().keys():
                    copy[key] = comment.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(comment)
                db.session.commit()
                return 'Deletion Successful', copy
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class UserComments(Resource):
    def get(self, user_id):
        if read_token(strip_token(request))['data']:
            if id_check(request, User, user_id) or read_token(strip_admin(request)):
                user_id = UUID(user_id)
                comments = Comment.by_user(user_id)
                return [comment.json() for comment in comments]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403
