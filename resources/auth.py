from flask_restful import Resource
from flask import request
from models.shelter import Shelter
from models.user import User
from middleware import create_token, gen_password, compare_password


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.by_id(data["user_id"])
        if user:
            if compare_password(data["password"], user.json()["password_digest"]):
                token = create_token(
                    {"id": str(user.id), "user_name": user.user_name})
                return token
            else:
                return 'Unauthorized', 404
        else:
            return 'Unauthorized', 404


class ShelterLogin(Resource):
    def post(self):
        data = request.get_json()
        shelter = Shelter.by_id(data["shelter_id"])
        if shelter:
            if compare_password(data["password"], shelter.json()["password_digest"]):
                token = create_token(
                    {"id": str(shelter.id), "shelter_name": shelter.shelter_name})
                return token
            else:
                return 'Unauthorized', 404
        else:
            return 'Unauthorized', 404


class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        data.update({"password_digest": gen_password(data["password"])})
        data.pop("password")
        user = User(**data)
        user.create()
        return user.json().pop("password_digest"), 201


class ShelterRegister(Resource):
    def post(self):
        data = request.get_json()
        data.update({"password_digest": gen_password(data["password"])})
        data.pop("password")
        shelter = Shelter(**data)
        shelter.create()
        return shelter.json().pop("password_digest"), 201
