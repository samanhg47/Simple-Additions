from middleware import admin_check, id_check, read_token, strip_token
from flask_restful import Resource
from models.comment import Comment
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID

from models.user import User
from resources.post import Posts


class AllComments(Resource):
    # def get(self):
    #     token = strip_token(request)
    #     if read_token(token)['data']:
    #         comments = Comment.find_all()
    #         return [comment.json() for comment in comments]
    #     else:
    #         return "Unauthorized", 403

    def post(self):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            params = {}
            for key in data.keys():
                params[key] = data[key]
            comment = Comment(**params)
            comment.create()
            return comment.json(), 201
        else:
            return "Unauthorized", 403


class Comments(Resource):
    #     def get(self, id):
    #         token = strip_token(request)
    #         if read_token(token)['data']:
    #             id = UUID(id)
    #             comment = Comment.by_id(id)
    #             if not comment:
    #                 return 'Comment Not Found', 404
    #             return comment.json().pop("password_digest")
    #         else:
    #             return "Unauthorized", 403

    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            if id_check(request, Comment, id) or admin_check(request):
                data = request.get_json()
                id = UUID(id)
                comment = Comment.by_id(id)
                if not comment:
                    return 'Comment Not Found', 404
                if not comment:
                    return 'Comment Not Found', 404
                for key in data.keys():
                    setattr(comment, key, data[key])
                db.session.commit()
                return comment.json()
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            if id_check(request, Comment, id) or admin_check(request):
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


# class PostComments(Resource):
#     def get(self, post_id):
#         token = strip_token(request)
#         if read_token(token)['data']:
#             comments = Comment.by_post(post_id)
#             return [comment.json() for comment in comments]
#         else:
#             return "Unauthorized", 403


class UserComments(Resource):
    def get(self, user_id):
        token = strip_token(request)
        if read_token(token)['data']:
            if id_check(request, User, user_id) or admin_check(request):
                user_id = UUID(user_id)
                comments = Comment.by_user(user_id)
                return [comment.json() for comment in comments]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403
