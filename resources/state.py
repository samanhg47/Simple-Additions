from middleware import read_token, strip_token
from models.state import State
from flask_restful import Resource
from flask import request


class By_Short(Resource):
    def get(self, state):
        state = State.by_shorthand(state)
        return state.json()


class States(Resource):
    def get(self):
        states = State.find_all()
        return [state.json() for state in states]


class By_Id(Resource):
    def get(self, id):
        state = State.by_id()
        return state.json()
