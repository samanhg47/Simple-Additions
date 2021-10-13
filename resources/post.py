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
    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            id = UUID(id)
            post = Post.by_id(id)
            for key in data.keys():
                setattr(post, key, data[key])
            db.session.commit()
            return post.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            post = Post.by_id(id)
            if not post:
                return {'msg': 'Post Not Found'}
            copy = {}
            for key in post.json().keys():
                copy[key] = post.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(post)
            db.session.commit()
            return {'Deletion Successful': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class ShelterPosts(Resource):
    def get(self, shelter_id):
        token = strip_token(request)
        if read_token(token)['data']:
            posts = Post.by_shelter_id(shelter_id)
            return [post.json() for post in posts]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
