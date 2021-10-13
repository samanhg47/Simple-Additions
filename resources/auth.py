from flask_restful import Resource
from flask import request
from models.user import User
from middleware import create_token, gen_password, compare_password


class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.by_id(data["user_id"])
        if user:
            if compare_password(data["password"], user.json()["password_digest"]):
                token = create_token(
                    {"id": str(user.id), "user_name": user.user_name})
                return token, 200
        else:
            return 'Unauthorized', 404


class Register(Resource):
    def post(self):
        data = request.get_json()
        params = {
            "user_name": data["user_name"],
            "password_digest": gen_password(data["password"])
        }
        user = User(**params)
        user.create()
        print(user.json())
        return user.json(), 201
