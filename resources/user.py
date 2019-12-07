from flask_restful import Resource, reqparse
from models.user import insert_to_table


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
        insert_to_table(**data)
        return {"message": "User created successfully"}, 201
