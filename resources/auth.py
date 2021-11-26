from middleware import create_token, gen_password, compare_password, token_user
from flask_restful import Resource
from models.shelter import Shelter
from models.user import User
from flask import request, make_response
from datetime import datetime, timedelta


class ShelterLogin(Resource):
    def post(self):
        data = request.get_json()
        data['email'] = data['email'].lower()
        shelter = Shelter.by_address(data['shelter_name'], data['address'])
        if shelter:
            shelter = shelter.json()
            if compare_password(data['password'], shelter['password_digest']):
                token = create_token(
                    {
                        "id": str(shelter['id']),
                        "shelter_name": shelter['shelter_name'],
                        "exp": datetime.utcnow() + timedelta(weeks=1),
                        "admin": False
                    }
                )
                res = make_response(shelter, 200)
                res.set_cookie(
                    'token',
                    value=token,
                    httponly=True,
                    samesite='strict',
                    # secure=True,
                    expires=(datetime.utcnow() + timedelta(weeks=1))
                )
                return res
            else:
                return '', 401
        else:
            return 'Shelter Not Found', 404


class UserLogin(Resource):
    def post(self):
        print()
        print()
        print('user', request.json)
        print()
        print()
        data = request.get_json()
        data['email'] = data['email'].lower()
        user = User.by_email(data['email'])
        if user:
            user = user.json()
            if compare_password(data['password'], user['password_digest']):
                if user['email'] == 'samangriffiths47@gmail.com':
                    token = create_token(
                        {
                            "id": str(user['id']),
                            "user_name": user['user_name'],
                            "exp": datetime.utcnow() + timedelta(weeks=1),
                            "admin": True
                        }
                    )
                else:
                    token = create_token(
                        {
                            "id": str(user['id']),
                            "user_name": user['user_name'],
                            "exp": datetime.utcnow() + timedelta(weeks=1),
                            "admin": False
                        }
                    )
                del user['password_digest']
                res = make_response({'user': user}, 200)
                res.set_cookie(
                    'token',
                    token,
                    # secure=True,
                    expires=(datetime.utcnow() + timedelta(weeks=1))
                )
                return res
            else:
                return '', 401
        else:
            return 'No User Found With That Email <br/> Please Either Register This Email Or Check Your Spelling', 404


class Token(Resource):
    def get(self):
        return token_user(request)


class UserRegister(Resource):
    def post(self):
        data = request.json
        data['email'] = data['email'].lower()
        if User.by_email(data['email']):
            return '''A User Has Already Registered With This Email <br/>
            Please Either Login Or Register With A Different Email''', 403
        else:
            data.update(
                {"password_digest": gen_password(data['password'])})
            del data['password']
            user = User(**data)
            user.create()
            user = user.json()
            del user['password_digest']
            return user, 201


class ShelterRegister(Resource):
    def post(self):
        data = request.get_json()
        data['email'] = data['email'].lower()
        if Shelter.by_address(data['shelter_name'], data['address']):
            shelter = Shelter.by_address(data['shelter_name'], data['address'])
            a = "A"
            if shelter.json()['shelter_name'][0] in ["A", "E", "I", "O", "U"]:
                a = "An"
            return """{} {} Already Exists At {}<br/>
            Either Log In Or Choose Another Shelter Name Or Location
            """.format(a, shelter.json()['shelter_name'], shelter.json()['address']), 403
        else:
            data.update({"password_digest": gen_password(data['password'])})
            del data['password']
            shelter = Shelter(**data)
            shelter.create()
            shelter = shelter.json()
            del shelter['password_digest']
            return shelter, 201
