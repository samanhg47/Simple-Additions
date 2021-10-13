from middleware import read_token, strip_token
from flask_restful import Resource
from models.comment import Comment
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID


class AllComments(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            comments = Comment.find_all()
            return [comment.json() for comment in comments]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

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
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class Comments(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            comment = Comment.by_id(id)
            return comment.json().pop("password_digest")
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def patch(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            id = UUID(id)
            comment = Comment.by_id(id)
            for key in data.keys():
                setattr(comment, key, data[key])
            db.session.commit()
            return comment.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            comment = Comment.by_id(id)
            if not comment:
                return {'msg': 'comment Not Found'}
            copy = {}
            for key in comment.json().keys():
                copy[key] = comment.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(comment)
            db.session.commit()
            return {'Deletion Successful': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class PostComments(Resource):
    def get(self, post_id):
        token = strip_token(request)
        if read_token(token)['data']:
            comments = Comment.by_post(post_id)
            return [comment.json() for comment in comments]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
