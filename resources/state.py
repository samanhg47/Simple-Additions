from models.state import State
from flask_restful import Resource
from flask import make_response


class By_Short(Resource):
    def get(self, state):
        state = State.by_shorthand(state)
        if state:
            return state.json()
        else:
            return "State Not Found", 404


class States(Resource):
    def get(self):
        states = State.find_all()
        if states:
            return [state.json() for state in states]
        else:
            return "States Not Found", 404


class State_Id(Resource):
    def get(self, id):
        state = State.by_id(id)
        if state:
            return state.json()
        else:
            return "State Not Found", 404
