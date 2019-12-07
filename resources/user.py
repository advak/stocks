from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
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

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "User with that email already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201
