from flask import request
import jwt
from app_init_file import app
from models.user import UserModel


def validate_token(func):
    def wrapper(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if not token:
                return {"message": "Token is missing"}
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'])
                current_user = UserModel.find_by_public_id(data["public_id"])
            except:
                return {"message": "Token is invalid"}, 401

            return func(*args, **kwargs, current_user=current_user)
    return wrapper
