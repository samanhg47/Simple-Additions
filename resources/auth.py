from middleware import create_token, gen_password, compare_password, token_user
from datetime import datetime, timedelta
from flask import request, make_response
from flask_restful import Resource
from models.shelter import Shelter
from models.user import User
from gevent import sleep
import requests
import os

GOOGLE_KEY = os.getenv("GOOGLE_KEY")


class ShelterLogin(Resource):
    def post(self):
        data = request.get_json()
        shelter_meta = Shelter.by_address(
            data['shelter_name'], data['address'])
        if shelter_meta:
            if compare_password(data['password'], shelter_meta.password()):
                shelter = shelter_meta.json()
                token = create_token(
                    {
                        "id": str(shelter['id']),
                        "shelter_name": shelter['shelter_name'],
                        "exp": datetime.utcnow() + timedelta(weeks=1),
                        "admin": False
                    }
                )
                res = make_response({'shelter': shelter}, 200)
                res.set_cookie(
                    'token',
                    value=token,
                    httponly=True,
                    samesite='none',
                    secure=True,
                    expires=(datetime.utcnow() + timedelta(weeks=1))
                )
                return res
            else:
                return '', 401
        else:
            return '''No Shelter Found With That Name At That Address<br/> Please
            Either Register With This Information<br/> Or Check That Your Information Is Correct''', 404


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        data['email'] = data['email'].lower()
        user_meta = User.by_email(data['email'])
        if user_meta:
            if compare_password(data['password'], user_meta.password()):
                user = user_meta.json()
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
                resp = make_response({'user': user}, 200)
                resp.set_cookie(
                    'token',
                    value=token,
                    httponly=True,
                    samesite='none',
                    secure=True,
                    expires=(datetime.utcnow() + timedelta(weeks=1))
                )
                return resp
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
            return shelter, 201


class RevGeocode(Resource):
    def get(self, lat, lng):
        sleep(1)
        req = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={key}'.format(
            lat=lat, lng=lng, key=GOOGLE_KEY
        )
        geocode = requests.get(
            req, stream=True
        )
        return geocode.json()


class Geocode(Resource):
    def get(self, address, city, state):
        sleep(1)
        req = 'https://maps.googleapis.com/maps/api/geocode/json?address={address},+{city},+{state}&key={key}'.format(
            address=address, city=city, state=state, key=GOOGLE_KEY
        )
        geocode = requests.get(
            req, stream=True
        )
        return geocode.json()
