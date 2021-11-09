from middleware import create_token, gen_password, compare_password, read_token, strip_admin, strip_token
from flask_restful import Resource
from models.shelter import Shelter
from models.user import User
from flask import request


class ShelterLogin(Resource):
    def post(self):
        data = request.get_json()
        data['email'] = data['email'].lower()
        shelter = Shelter.by_address(data['shelter_name'], data['address'])
        if shelter:
            if compare_password(data['password'], shelter.json()['password_digest']):
                token = create_token(
                    {"id": str(shelter.id), "shelter_name": shelter['shelter_name']})
                return {"shelter": shelter, "token": token, 'admin': 'Shelter'}
            else:
                return 'Password Incorrect', 401
        else:
            return 'Shelter Not Found', 404


class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            data['email'] = data['email'].lower()

            user = User.by_email(data['email'])
        except:
            return 'Error', 404
        if compare_password(data['password'], user.json()['password_digest']):
            token = create_token(
                {"id": str(user.id), "user_name": user['user_name']})
            if user['email'] == 'samangriffiths47@gmail.com':
                admin = create_token(
                    {"id": user['id'], "user_name": user['user_name']}
                )
            else:
                admin = "User"
            del user['password_digest']
            return {"user": user, "token": token, 'admin': admin}
        else:
            return "Password Incorrect", 401

    def get(self):
        if read_token(strip_token(request)):
            if strip_admin(request):
                boolean = True
            else:
                boolean = False
        else:
            boolean = False
        return boolean


class UserRegister(Resource):
    def post(self):
        try:
            data = request.get_json()
            data['email'] = data['email'].lower()
            if User.by_email(data['email']):
                return "Profile Already Created With This Email", 403
            else:
                data.update(
                    {"password_digest": gen_password(data['password'])})
                del data['password']
                user = User(**data)
                user.create()
                user = user.json()
                del user['password_digest']
                return user, 201
        except 404:
            return "City Not Found", 404


class ShelterRegister(Resource):
    def post(self):
        data = request.get_json()
        data['email'] = data['email'].lower()
        shelter = Shelter.by_address(data['shelter_name'], data['address'])
        if shelter:
            a = "A"
            if shelter.json()['shelter_name'][0] in ["A", "E", "I", "O", "U"]:
                a = "An"
            return """Error: {} {} Already Exists In This Location.
            Choose Either Another Shelter Name Or Location.
            """.format(a, shelter.json()['shelter_name']), 403
        else:
            data.update({"password_digest": gen_password(data['password'])})
            del data['password']
            shelter = Shelter(**data)
            shelter.create()
            shelter = shelter.json()
            del shelter['password_digest']
            return shelter, 201
