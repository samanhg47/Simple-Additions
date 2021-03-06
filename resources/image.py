from middleware import check_admin, id_check
from flask_restful import Resource
from models.image import Image
from datetime import datetime
from flask import request
from models.db import db
from uuid import UUID


class AllImages(Resource):
    def post(self):
        data = request.get_json()
        params = {}
        for key in data.keys():
            params[key] = data[key]
        image = Image(**params)
        image.create()
        return image.json(), 201


class Images(Resource):
    def get(self, id):
        id = UUID(id)
        image = Image.by_id(id)
        if not image:
            return 'Image Not Found', 404
        return image.json()

    def patch(self, id):
        if id_check(request, Image, id) or check_admin(request):
            id = UUID(id)
            data = request.get_json()
            image = Image.by_id(id)
            if not image:
                return 'Image Not Found', 404
            for key in data.keys():
                setattr(image, key, data[key])
            db.session.commit()
            return image.json()
        else:
            return "Unauthorized", 403

    def delete(self, id):
        if id_check(request, Image, id) or check_admin(request):
            id = UUID(id)
            image = Image.by_id(id)
            if not image:
                return 'Image Not Found', 404
            copy = {}
            for key in image.json().keys():
                copy[key] = image.json()[key]
                copy['updated_at'] = str(datetime.utcnow())
            db.session.delete(image)
            db.session.commit()
            return 'Deletion Successful', copy
        else:
            return "Unauthorized", 403
