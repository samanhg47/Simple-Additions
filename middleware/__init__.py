from models.shelter import Shelter
from dotenv import load_dotenv
from models.user import User
from uuid import UUID
import bcrypt
import jwt
import os

load_dotenv()
SECRET_KEY = os.getenv('APP_SECRET')


def create_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def read_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.InvalidSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def gen_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def compare_password(password, hash_password):
    return bcrypt.checkpw(password.encode(), hash_password.encode())


def strip_token(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
        return token
    except:
        return None


def strip_admin(request):
    try:
        admin = request.headers['Admin']
        return admin
    except:
        return None


def id_check(request, model, model_id):
    try:
        id = request.headers['Id']
        if model == User and UUID(model_id) == UUID(id) or model == Shelter and UUID(model_id) == UUID(id):
            return True
        else:
            subject = model.by_id(model_id)
            if UUID(subject.json()['user_id']) == UUID(id):
                return True
            else:
                return False
    except:
        return None
