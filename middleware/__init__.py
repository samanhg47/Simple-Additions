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


def create_token(payload):
    return jwt.encode(
        payload,
        APP_SECRET,
        algorithm="HS256"
    )


def check_token(request):
    try:
        token = request.cookies.get('token')
    except:
        return False
    try:
        jwt.decode(token, APP_SECRET, algorithms=["HS256"])
        return True
    except:
        return False


def token_user(request):
    try:
        token = request.cookies.get('token')
    except:
        return None
    try:
        user = jwt.decode(token, APP_SECRET, algorithms=["HS256"])
        return user['id']
    except jwt.InvalidSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def gen_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def compare_password(password, hash_password):
    return bcrypt.checkpw(password.encode(), hash_password.encode())


def strip_secret(request):
    secret = request.headers['Secret']
    return compare_password(SECRET_KEY, secret)


def check_admin(request):
    try:
        token = request.cookies.get('token')
    except:
        return False
    try:
        admin = jwt.decode(token, APP_SECRET, algorithms=["HS256"])['admin']
        return admin
    except jwt.InvalidSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def id_check(request, model, model_id):
    try:
        id = token_user(request)
        if id:
            if model == User and UUID(model_id) == UUID(id) or model == Shelter and UUID(model_id) == UUID(id):
                return True
            else:
                subject = model.by_id(model_id)
                if subject:
                    if UUID(subject.json()['user_id']) == UUID(id):
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False
    except:
        return None
