from middleware import read_token, strip_token, admin_check
from dotenv.main import load_dotenv
from flask import request, jsonify
from models.shelter import Shelter
from flask_restful import Resource
from models.comment import Comment
from models.image import Image
from models.post import Post
from models.user import User
from models.db import db
import os

load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


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
                return "All Posts Successfully Deleted"
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


def censor_language(data):
    censored_words = [
        "bitch", "fuck", "shit",
        "cunt", "ass", "fag",
        "tranny", "hoe", "whore",
        "tits", "titt" "dick",
        "retard", "pussy", "dumb",
        "idiot", "stupid", "kill",
        "stab", "shoot"]
    text = data["body"].lower()
    for word in censored_words:
        if text.count(word) > 0:
            count = text.count(word)
            censored_word = ""
            for letter in word:
                censored_word += "*"
            data["body"] = data["body"].replace(word, censored_word, count)
            data["body"] = data["body"].replace(
                word.capitalize(), censored_word, count)
            data["body"] = data["body"].replace(
                word.upper(), censored_word, count)
    return data["body"]


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

    def delete(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                images = Image.find_all()
                for image in images:
                    db.session.delete(image)
                return "All Images Successfully Deleted"
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

    def delete(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                users = User.find_all()
                for user in users:
                    db.session.delete(user)
                return "All Users Successfully Deleted"
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

    def delete(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                comments = Comment.find_all()
                for comment in comments:
                    db.session.delete(comment)
                return "All Comments Successfully Deleted"
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class AllShelters(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                shelters = Shelter.find_all()
                return [shelter.json() for shelter in shelters]
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self):
        token = strip_token(request)
        if read_token(token):
            if admin_check(request):
                shelters = Shelter.find_all()
                for shelter in shelters:
                    db.session.delete(shelter)
                return "All Shelters Successfully Deleted"
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class AllUploads(Resource):
    def list_files():
        token = strip_token(request)
        if read_token(token):
            files = []
            for filename in os.listdir(UPLOAD_DIRECTORY):
                path = os.path.join(UPLOAD_DIRECTORY, filename)
                if os.path.isfile(path):
                    files.append(filename)
            return jsonify(files)
        else:
            return "Unauthorized", 403
