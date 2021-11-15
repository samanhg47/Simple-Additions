from models.shelter import Shelter
from dotenv import load_dotenv
from models.user import User
from uuid import UUID
import bcrypt
import jwt
import os

load_dotenv()
APP_SECRET = os.getenv('APP_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')
SALT = int(os.getenv('SALT_ROUNDS'))


def create_token(payload):
    return jwt.encode(
        payload,
        APP_SECRET,
        algorithm="HS256"
    )


def read_token(token):
    try:
        jwt.decode(token, APP_SECRET, algorithms=["HS256"])
        return True
    except jwt.InvalidSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def gen_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(SALT)).decode()


def compare_password(password, hash_password):
    return bcrypt.checkpw(password.encode(), hash_password.encode())


def strip_token(request):
    try:
        token = request.cookies.get('token')
        return token
    except:
        return None


def strip_secret(request):
    secret = request.headers['Secret']
    return compare_password(SECRET_KEY, secret)


def strip_admin(token):
    try:
        admin = jwt.decode(token, APP_SECRET, algorithms=["HS256"])['admin']
        return admin
    except:
        return False


def check_admin(request):
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
