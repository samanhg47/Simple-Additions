from sqlalchemy.orm.query import _ColumnEntity
from middleware import read_token, strip_token
from models.city import City
from flask_restful import Resource
from flask import request


class By_State(Resource):
    def get(self, state):
        cities = City.by_state(state)
        return [city.json() for city in cities]


class Detailed(Resource):
    def get(self, state, name, zipcode):
        city = City.by_info(state, name, zipcode)
        return city.json()


class By_Id(Resource):
    def get(self, id):
        city = City.by_id(id)
        return city.json()
