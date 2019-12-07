from flask import Flask
from flask_restful import Api
from resources.user import UserRegister


app = Flask(__name__)
api = Api(app)
api.add_resource(UserRegister, '/register')
app.run(port=5000, debug=True)
