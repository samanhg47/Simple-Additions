from middleware import read_token, strip_token
from flask_restful import Resource
from datetime import datetime
from models import image
from models.image import Image
from flask import request
from models.db import db
from uuid import UUID


class AllImages(Resource):
    def get(self):
        token = strip_token(request)
        if read_token(token)['data']:
            images = Image.find_all()
            return [image.json() for image in images]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def post(self):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            params = {}
            for key in data.keys():
                params[key] = data[key]
            image = Image(**params)
            image.create()
            return image.json(), 201
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class Images(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token)['data']:
            id = UUID(id)
            image = Image.by_id(id)
            return image.json().pop("password_digest")
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def patch(self, image_id):
        token = strip_token(request)
        if read_token(token)['data']:
            data = request.get_json()
            image_id = UUID(image_id)
            image = Image.find_by_id(image_id)
            for key in data.keys():
                setattr(image, key, data[key])
            db.session.commit()
            return image.json()
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]

    def delete(self, image_id):
        token = strip_token(request)
        if read_token(token)['data']:
            image_id = UUID(image_id)
            image = Image.find_by_id(image_id)
            if not image:
                return {'msg': 'image Not Found'}
            copy = {}
            for key in image.json().keys():
                copy[key] = image.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(image)
            db.session.commit()
            return {'Deletion Successful': copy}
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]


class PostImages(Resource):
    def get(self, post_id):
        token = strip_token(request)
        if read_token(token)['data']:
            images = Image.by_post_id(post_id)
            return [image.json() for image in images]
        else:
            return read_token(token)['payload'][0], read_token(token)['payload'][1]
