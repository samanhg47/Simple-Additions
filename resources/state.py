from middleware import read_token, strip_token
from models.state import State
from flask_restful import Resource
from flask import request


class By_Short(Resource):
    def get(self, state):
        token = strip_token(request)
        if read_token(token):
            state = State.by_shorthand(state)
            return state.json()
        else:
            return "Unauthorized", 401
