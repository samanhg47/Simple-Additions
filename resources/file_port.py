from flask import request, redirect, url_for, send_from_directory
from middleware import read_token, strip_token
from werkzeug.utils import secure_filename
from dotenv.main import load_dotenv
from flask_restful import Resource
import random
import os

load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return filename.count('.') == 1 and \
        filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS \
        and "/" not in filename


def random_address():
    str = "zaxsc15387"
    address = ""
    for char in random.choices(str):
        address += char
    return address + "/"


class Uploads(Resource):
    def post():
        token = strip_token(request)
        if read_token(token):
            if 'file' not in request.files:
                return "No File Uploaded", 403
            file = request.files['file']
            if file.filename == '':
                return "File Format Not Accepted", 403
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = random_address() + filename
                file.save(os.path.join(UPLOAD_DIRECTORY, filename))
                redirect(url_for('download_file', name=filename))
                return filename, 201
            else:
                return "File Format Not Accepted", 403
        else:
            return "Unauthorized", 403


class Downloads(Resource):
    def download_file(name):
        return send_from_directory(UPLOAD_DIRECTORY, name)
