from flask_restful import Resource
from flask_cors import cross_origin
from flask import request, make_response, jsonify
from werkzeug.wrappers import response
from models.shelter import Shelter
from models.user import User
from middleware import admin_check, create_token, gen_password, compare_password, read_token, strip_token


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
        response = make_response(
            jsonify(
                {"message": "REQUEST SUCCESSFUL"}
            ), 201
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        # if request.method == "OPTIONS":
        #   response.wr
        return response


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

    # response = jsonify(message="Simple server is running")

    # # Enable Access-Control-Allow-Origin
    # response.headers.add("Access-Control-Allow-Origin", "*")
    # return response
