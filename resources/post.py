import json
from middleware import read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models.post import Post
from flask import request
from models.db import db
from uuid import UUID


class AllPosts(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            posts = Post.find_all()
            return [post.json() for post in posts]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def post(self):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            params = {}
            for key in data.keys():
                params[key] = data[key]
            post = Post(**params)
            post.create()
            return post.json(), 201
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class Posts(Resource):
    def patch(self, post_id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            post_id = UUID(post_id)
            post = Post.find_by_id(post_id)
            for key in data.keys():
                setattr(post, key, data[key])
            db.session.commit()
            return post.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, post_id):
        token = strip_token(request)
        if read_token(token)['data']:
            post_id = UUID(post_id)
            post = Post.find_by_id(post_id)
            if not post:
                return {'msg': 'Post Not Found'}
            copy = {}
            for key in post.json().keys():
                copy[key] = post.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(post)
            db.session.commit()
            return {'msg': 'Post Deletion Successful', 'payload': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class UserPosts(Resource):
    def get(self, user_name):
        token = strip_token(request)
        if read_token(token)['data']:
            posts = Post.find_by_user_name(user_name)
            return posts
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
