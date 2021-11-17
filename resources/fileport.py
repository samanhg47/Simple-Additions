from gevent import sleep
from flask import request
from dotenv.main import load_dotenv
from flask_restful import Resource
from random import randbytes
import os
import boto3
load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
S3_ADMIN_ID = os.getenv("S3_ADMIN_ID")
S3_ADMIN_SECRET = os.getenv("S3_ADMIN_SECRET")
S3_REGION = os.getenv("S3_REGION")
S3_USER_ID = os.getenv("S3_USER_ID")
S3_USER_SECRET = os.getenv("S3_USER_SECRET")


class S3Upload(Resource):
    def get(self):
        sleep(1)
        s3_user = boto3.client(
            's3',
            aws_access_key_id=S3_USER_ID,
            aws_secret_access_key=S3_USER_SECRET,
            region_name=S3_REGION
        )
        image_name = str(randbytes(16), "UTF-16")
        params = {
            "Bucket": S3_BUCKET,
            "Key": image_name
        }
        response = s3_user.generate_presigned_url(
            'put_object', Params=params, ExpiresIn=5)
        return response


class S3Delete(Resource):
    def delete(self, key):
        sleep(1)
        data = request.get_json()
        key = data["key"]
        s3_user = boto3.client(
            's3',
            aws_access_key_id=S3_ADMIN_ID,
            aws_secret_access_key=S3_ADMIN_SECRET,
            region_name=S3_REGION
        )
        s3_user.delete_object(Bucket=S3_BUCKET, KEY=key)
