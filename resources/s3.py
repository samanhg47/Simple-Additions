from dotenv import load_dotenv, find_dotenv
import os
import logging
import boto3
from botocore.exceptions import ClientError


load_dotenv(find_dotenv())

S3_BUCKET = os.getenv("S3_BUCKET")
S3_USER_KEY = os.getenv("S3_USER_ID")
S3_USER_SECRET = os.getenv("S3_USER_SECRET")
S3_ADMIN_KEY = os.getenv("S3_ADMIN_ID")
S3_ADMIN_SECRET = os.getenv("S3_ADMIN_SECRET")


def generate_bucket_url(image_name):
    s3_user = boto3.client(
        's3',
        aws_access_key_id=S3_USER_KEY,
        aws_secret_access_key=S3_USER_SECRET
    )

    params = {
        "Bucket": S3_BUCKET,
        "Key": str(image_name)
    }

    try:
        response = s3_user.generate_presigned_url(
            'put_object', params, ExpiresIn=60)
    except ClientError as e:
        logging.error(e)
        return None
    return response
