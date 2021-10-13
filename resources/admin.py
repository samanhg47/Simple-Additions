from middleware import read_token, strip_token, admin_check
from flask_restful import Resource
from models.comment import Comment
from models.image import Image
from models.post import Post
from models.user import User
from flask import request
from models.db import db


class AllPosts(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                posts = Post.find_all()
                return [post.json() for post in posts]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                posts = Post.find_all()
                for post in posts:
                    db.session.delete(post)
                return "All posts successfully deleted"
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class AllImages(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                images = Image.find_all()
                return [image.json() for image in images]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class AllUsers(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                users = User.find_all()
                return [user.json() for user in users]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class AllComments(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                comments = Comment.find_all()
                return [comment.json() for comment in comments]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403
