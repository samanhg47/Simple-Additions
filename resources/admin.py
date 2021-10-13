from middleware import read_token, strip_token, admin_check
from flask_restful import Resource
from datetime import datetime
from models.post import Post
from flask import request
from models.db import db


class AllPosts(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            if admin_check(request):
                posts = Post.find_all()
                return [post.json() for post in posts]
            else:
                return "Unauthorized", 403
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self):
        token = strip_token(request)
        if read_token(token)['data']:
            if admin_check(request):
                posts = Post.find_all()
                for post in posts:
                    db.session.delete(post)
                return "All posts successfully deleted"
            else:
                return "Unauthorized", 403
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
