from flask_restful import Resource
from flask import request
from models.shelter import Shelter
from models.user import User
from middleware import admin_check, create_token, gen_password, compare_password


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.by_name(data["user_name"])
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
        shelter = Shelter.by_contacts(
            data["phone_number"], data["email"], data["shelter_name"], data["address"])
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
        user = User.by_name(data["user_name"])
        if user:
            return "Error: Username Taken", 403
        data.update({"password_digest": gen_password(data["password"])})
        del data["password"]
        user = User(**data)
        user.create()
        user = user.json()
        if admin_check(request):
            return user, 201
        del user["password_digest"]
        del user["id"]
        return user, 201


class ShelterRegister(Resource):
    def post(self):
        data = request.get_json()
        shelter = Shelter.by_contacts(
            data["phone_number"], data["email"], data["shelter_name"], data["address"])
        if shelter:
            a = "A"
            if shelter.json()["shelter_name"][0] in ["A", "E", "I", "O", "U"]:
                a = "An"
            return "Error: {} {} Already Exists In This Location".format(a, shelter.json()["shelter_name"]), 403
        data.update({"password_digest": gen_password(data["password"])})
        del data["password"]
        shelter = Shelter(**data)
        shelter.create()
        shelter = shelter.json()
        if admin_check(request):
            return shelter, 201
        del shelter["password_digest"]
        del shelter["id"]
        return shelter, 201
