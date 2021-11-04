from logging import error
from flask_restful import Resource
from flask_cors import cross_origin
from flask import request, make_response, jsonify
from werkzeug.wrappers import response
from models.shelter import Shelter
from models.user import User
from uuid import UUID
from middleware import admin_check, create_token, gen_password, compare_password, read_token, strip_token


class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = User.by_name(data["user_name"])
            user.json()
        except:
            return "User Not Found", 404
        try:
            user = User.by_name(data["user_name"])
            if compare_password(data["password"], user.json()["password_digest"]):
                token = create_token(
                    {"id": str(user.id), "user_name": user.user_name})
                user = user.json()
                del user["password_digest"]
                return {"user": user, "token": token}
        except:
            return "Password Incorrect, Try Again.", 401

    def get(self):
        token = strip_token(request)
        bool = read_token(token)
        return bool


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
                return 'Unauthorized', 403
        else:
            return 'Unauthorized', 403


class UserRegister(Resource):
    def post(self):
        try:
            data = request.get_json()
            data.update(
                {"password_digest": gen_password(data["password"])})
            del data["password"]
            user = User(**data)
            user.create()
            user = user.json()
            # if admin_check(request):
            #     return user, 201
            # del user["password_digest"]
            return user, 201
        except:
            return "Error Occured", 401


class ShelterRegister(Resource):
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
                a = "A"
                if shelter.json()["shelter_name"][0] in ["A", "E", "I", "O", "U"]:
                    a = "An"
                return """Error: {} {} Already Exists In This Location.
                If You Are Registering, Choose Either Another Shelter Name Or Location.
                If You Are Logining In As The Before Mentioned Shelter, Try Again.
                """.format(a, shelter.json()["shelter_name"]), 403
        data.update({"password_digest": gen_password(data["password"])})
        del data["password"]
        shelter = Shelter(**data)
        shelter.create()
        shelter = shelter.json()
        if admin_check(request):
            return shelter, 201
        del shelter["password_digest"]
        token = create_token(
            {"id": str(shelter.id), "shelter_name": shelter.shelter_name})
        return {"shelter": shelter, "token": token}, 201
