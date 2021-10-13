from flask import request, abort, jsonify, send_from_directory
from middleware import read_token, strip_token, admin_check, id_check
from flask_restful import Resource
from dotenv import load_dotenv
from datetime import datetime
from models.post import Post
from models.db import db
from uuid import UUID
import os

from models.user import User

load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")


class AllPosts(Resource):
    def post(self):
        token = strip_token(request)
        if read_token(token):
            data = request.get_json()
            params = {}
            for key in data.keys():
                params[key] = data[key]
            post = Post(**params)
            post.create()
            return post.json(), 201
        else:
            return "Unauthorized", 403


class Posts(Resource):
    def patch(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, Post, id) or admin_check(request):
                data = request.get_json()
                id = UUID(id)
                post = Post.by_id(id)
                for key in data.keys():
                    setattr(post, key, data[key])
                db.session.commit()
                return post.json()
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, Post, id) or admin_check(request):
                id = UUID(id)
                post = Post.by_id(id)
                if not post:
                    return {'msg': 'Post Not Found'}, 404
                copy = {}
                for key in post.json().keys():
                    copy[key] = post.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(post)
                db.session.commit()
                return 'Deletion Successful', copy
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


# class ShelterPosts(Resource):
#     def get(self, shelter_id):
#         token = strip_token(request)
#         if read_token(token):
#             shelter_id = UUID(shelter_id)
#             posts = Post.by_shelter(shelter_id)
#             return [post.json() for post in posts]
#         else:
#             return "Unauthorized", 403


class UserPosts(Resource):
    def get(self, user_id):
        token = strip_token(request)
        if read_token(token):
            if id_check(request, User, user_id) or admin_check(request):
                user_id = UUID(user_id)
                posts = Post.by_user(user_id)
                return [post.json() for post in posts]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403
