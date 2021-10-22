from models.city import City
from flask_restful import Resource


class By_State(Resource):
    def get(self, state):
        cities = City.by_state(state)
        if cities:
            return [{
                "zipcode": city.json()["zipcode"],
                "city":city.json()["city"],
                "state": city.json()["state_name"]}
                for city in cities]
        else:
            return "Cities Not Found", 404


class Detailed(Resource):
    def get(self, state, name, zipcode):
        city = City.by_info(state, name, zipcode)
        if city:
            return city.json()
        else:
            return "City Not Found", 404


class City_Id(Resource):
    def get(self, id):
        city = City.by_id(id)
        if city:
            return city.json()
        else:
            return "City Not Found", 404
