from flask_restful import Api
from resources.user import UserSignUp, UserSignIn
from resources.portfolio import Portfolio
from resources.stock import Stock
from app_init_file import app

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserSignUp, '/sign_up')
api.add_resource(UserSignIn, '/sign_in')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(Stock, '/stock')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
