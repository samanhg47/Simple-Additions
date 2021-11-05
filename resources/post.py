import requests
from middleware import read_token, strip_token, strip_admin, id_check
from resources.admin import censor_language
from flask_restful import Resource
from datetime import datetime
from models.user import User
from models.post import Post
from flask import request
from models.db import db
from uuid import UUID
import os


class AllPosts(Resource):
    def post(self):
        if read_token(strip_token(request)):
            data = request.get_json()
            data["body"] = censor_language(data)
            post = Post(**data)
            post.create()
            return post.json(), 201
        else:
            return "Unauthorized", 401


class Posts(Resource):
    def get(self, id):
        if read_token(strip_token(request)):
            if id_check(request, Post, id) or read_token(strip_admin(request)):
                id = UUID(id)
                post = Post.by_id(id)
                if not post:
                    return 'Post Not Found', 404
                return post.json()

    def patch(self, id):
        if read_token(strip_token(request)):
            if id_check(request, Post, id) or read_token(strip_admin(request)):
                data = request.get_json()
                data["body"] = censor_language(data)
                id = UUID(id)
                post = Post.by_id(id)
                if not post:
                    return 'Post Not Found', 404
                for key in data.keys():
                    setattr(post, key, data[key])
                db.session.commit()
                return post.json()
            else:
                return "This Method Is Inaccessable", 403
        else:
            return "Unauthorized", 401

    def delete(self, id):
        if read_token(strip_token(request)):
            if id_check(request, Post, id) or read_token(strip_admin(request)):
                id = UUID(id)
                post = Post.by_id(id)
                if not post:
                    return 'Post Not Found', 404
                copy = {}
                for key in post.json().keys():
                    copy[key] = post.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(post)
                db.session.commit()
                return 'Deletion Successful', copy
            else:
                return "This Method Is Inaccessable", 403
        else:
            return "Unauthorized", 401


class UserPosts(Resource):
    def get(self, user_id):
        if read_token(strip_token(request)):
            if id_check(request, User, user_id) or read_token(strip_admin(request)):
                user_id = UUID(user_id)
                posts = Post.by_user(user_id)
                return [post.json() for post in posts]
            else:
                return "This Method Is Inaccessable", 403
        else:
            return "Unauthorized", 401
