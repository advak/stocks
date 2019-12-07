from flask import Flask
from flask_restful import Api
from resources.user import UserSignUp, UserSignIn


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserSignUp, '/sign_up')
api.add_resource(UserSignIn, '/sign_in')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
