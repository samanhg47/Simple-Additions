from middleware import read_token, strip_token, strip_admin
from dotenv.main import load_dotenv
from flask import request
from models.shelter import Shelter
from flask_restful import Resource
from models.comment import Comment
from models.image import Image
from models.post import Post
from models.user import User
from models.db import db

load_dotenv()


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


class AdminAllPosts(Resource):
    def get(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                posts = Post.find_all()
                return [post.json() for post in posts]
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401

    def delete(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                posts = Post.find_all()
                for post in posts:
                    db.session.delete(post)
                db.session.commit()
                return "All Posts Successfully Deleted"
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401


class AdminAllImages(Resource):
    def get(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                images = Image.find_all()
                return [image.json() for image in images]
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401

    def delete(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                images = Image.find_all()
                for image in images:
                    db.session.delete(image)
                return "All Images Successfully Deleted"
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401


class AdminAllUsers(Resource):
    def get(self):
        # if read_token(strip_token(request)):
        #     if read_token(strip_admin(request)):
        users = User.find_all()
        allUsers = [user.json() for user in users]
        return allUsers
        #     else:
        #         return "Not Admin", 401
        # else:
        #     return "Unauthenticated", 401

    def delete(self):
        # if read_token(strip_token(request)):
        #     if read_token(strip_admin(request)):
        users = User.find_all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return "All Users Successfully Deleted"
        #     else:
        #         return "Not Admin", 401
        # else:
        #     return "Unauthenticated", 401


class AdminAllComments(Resource):
    def get(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                comments = Comment.find_all()
                return [comment.json() for comment in comments]
            else:
                return "Unauthorized", 401
        else:
            return "Unauthorized", 401

    def delete(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                comments = Comment.find_all()
                for comment in comments:
                    db.session.delete(comment)
                db.session.commit()
                return "All Comments Successfully Deleted"
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401


class AdminAllShelters(Resource):
    def get(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                shelters = Shelter.find_all()
                return [shelter.json() for shelter in shelters]
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401

    def delete(self):
        if read_token(strip_token(request)):
            if read_token(strip_admin(request)):
                shelters = Shelter.find_all()
                for shelter in shelters:
                    db.session.delete(shelter)
                db.session.commit()
                return "All Shelters Successfully Deleted"
            else:
                return "Not Admin", 401
        else:
            return "Unauthenticated", 401
