from flask_restful import Resource, reqparse
from models.user import UserModel
from models.portfolio import PortfolioModel
import jwt
import datetime
from app_init_file import app


class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('portfolio_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserSignUp.parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "User with that email already exists"}, 400
        user = UserModel(data["email"], data["first_name"], data["last_name"])
        user.set_password(data["password"])
        user.save_to_db()

        portfolio = PortfolioModel(data["portfolio_name"], owner=user)
        portfolio.save_to_db()

        return {"message": "User created successfully"}, 201


class UserSignIn(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserSignIn.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "There is no signed up user with this email"}, 401
        if user.check_password(data["password"]):
            token = jwt.encode(
                {'public_id': user.public_id,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])
            return {'token': token.decode('UTF-8')}

        else:
            return {'message': "Password is incorrect"}, 401

