import bcrypt
import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('APP_SECRET')


def create_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def read_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {'data': True, "payload": payload}
    except jwt.InvalidSignatureError:
        return {'data': False, "payload": {'msg': "Unauthorized", 'error': 404}}
    except jwt.InvalidTokenError:
        return {'data': False, "payload": {'msg': "Unauthorized", 'error': 404}}


def gen_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def compare_password(password, hash_password):
    return bcrypt.checkpw(password.encode(), hash_password.encode())


def strip_token(req):
    try:
        token = req.headers['Authorization'].split(' ')[1]
        print(req)
        return token
    except:
        return None
