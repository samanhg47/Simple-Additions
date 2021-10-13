from middleware import admin_check, id_check, read_token, strip_token
from flask_restful import Resource
from models.image import Image
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID


class AllImages(Resource):
    def post(self):
        token = strip_token(request)
        if read_token(token):
            data = request.get_json()
            params = {}
            for key in data.keys():
                params[key] = data[key]
            image = Image(**params)
            image.create()
            return image.json(), 201
        else:
            return "Unauthorized", 403


class Images(Resource):
    def get(self, id):
        token = strip_token(request)
        if read_token(token):
            id = UUID(id)
            image = Image.by_id(id)
            return image.json().pop("password_digest")
        else:
            return "Unauthorized", 403

    def patch(self, id):
        token = strip_token(request)
        if read_token(token):
            data = request.get_json()
            id = UUID(id)
            image = Image.by_id(id)
            if id_check(request, Image, id) or admin_check(request):
                for key in data.keys():
                    setattr(image, key, data[key])
                db.session.commit()
                return image.json()
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403

    def delete(self, id):
        token = strip_token(request)
        if read_token(token):
            id = UUID(id)
            image = Image.by_id(id)
            if not image:
                return {'msg': 'image Not Found'}
            if id_check(request, Image, id) or admin_check(request):
                copy = {}
                for key in image.json().keys():
                    copy[key] = image.json()[key]
                    copy['updated_at'] = str(datetime.utcnow())
                db.session.delete(image)
                db.session.commit()
                return {'Deletion Successful': copy}
            else:
                return "Unauthorized", 403
        else:
            return "Unauthorized", 403


class PostImages(Resource):
    def get(self, post_id):
        token = strip_token(request)
        if read_token(token):
            images = Image.by_post(post_id)
            return [image.json() for image in images]
        else:
            return "Unauthorized", 403
