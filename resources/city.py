import requests
from middleware import read_token, strip_token, admin_check, id_check
from models.city import City
from resources.admin import censor_language
from flask_restful import Resource
from datetime import datetime
from models.user import User
from models.post import Post
from flask import request
from models.db import db
from uuid import UUID
import os


class AllCities(Resource):
    def get(self):
        cities = City.find_all()
        token = strip_token(request)
        if read_token(token):
            return [city.json() for city in cities]
        else:
            return "Unauthorized", 401
