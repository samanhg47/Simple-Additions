from flask_restful import Resource
from flask import request
from models.shelter import Shelter
from models.user import User
from middleware import create_token, gen_password, compare_password, read_token, strip_admin, strip_token


class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user = User.by_name(data.user_name)
            user.json()
            user = User.by_name(data.user_name)
            if compare_password(data["password"], user.json()["password_digest"]):
                token = create_token(
                    {"id": str(user.id), "user_name": user.user_name})
                user = user.json()
                if user.user_name == 'Saman':
                    admin = create_token(
                        {"id": user.id, "user_name": user.user_name})
                else:
                    admin = "Not Admin"
                del user["password_digest"]
                return {"user": user, "token": token, 'admin': admin}
        except 401:
            return "Password Incorrect, Try Again.", 401
        except 404:
            return "User Not Found", 404

    def get(self):
        if read_token(strip_token(request)):
            if strip_admin(request):
                boolean = True
            else:
                boolean = False
        else:
            boolean = False
        return boolean


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
            del user["password_digest"]
            return user, 201
        except:
            return "Error Occured", 401


class ShelterRegister(Resource):
    def post(self):
        data = request.get_json()
        shelter = Shelter.by_contacts(
            data["phone_number"], data["email"], data["shelter_name"], data["address"])

        if shelter:
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
        token = create_token(
            {"id": str(shelter.id), "shelter_name": shelter.shelter_name})
        del shelter["password_digest"]
        return shelter, 201
