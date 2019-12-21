from flask_restful import Resource, reqparse
from models.user import UserModel
from models.portfolio import PortfolioModel


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
            return {"message": "There is no signed up user with this email"}, 400
        password_validation = user.check_password(data["password"])
        if not password_validation:
            return {"message": "Incorrect password"}, 401

        return {"message": "User authenticated successfully"}, 201
