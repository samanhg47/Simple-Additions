
from flask import Flask, request, abort, jsonify, send_from_directory
from middleware import read_token, strip_token
from dotenv.main import load_dotenv
from flask_restful import Resource
import os


load_dotenv()

UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY")


def post_file(filename):
    if "/" in filename:
        abort(400, "no subdirectories allowed")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    return "File Created", 201


class AllFiles(Resource):
    def list_files():
        token = strip_token(request)
        if read_token(token):
            files = []
            for filename in os.listdir(UPLOAD_DIRECTORY):
                path = os.path.join(UPLOAD_DIRECTORY, filename)
                if os.path.isfile(path):
                    files.append(filename)
            return jsonify(files)
        else:
            return "Unauthorized", 403


class SingleFile(Resource):
    def get_file(path):
        return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)
