from middleware import read_token, strip_token
from models.city import City
from flask_restful import Resource
from flask import request


class By_State(Resource):
    def get(self, state):
        token = strip_token(request)
        if read_token(token):
            cities = City.by_state(state)
            return [city.json() for city in cities]
        else:
            return "Unauthorized", 401
