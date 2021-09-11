from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'y6_7#d9&l^5l5@$ob%4&kk70j@jdmq=h0b(b^9r0$9%@jn#x2%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5434/flask_bmg'

db = SQLAlchemy()
bcrpyt = Bcrypt()
api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.init_app(app)
    bcrpyt.init_app(app)
    db.create_all()


from flask_app.resources.hero import Hero
from flask_app.resources.login import Login
from flask_app.resources.register import Register
from flask_app.resources.referral import Referral
from flask_app.resources.user import User

api.add_resource(Hero, '/hero/<string:name>')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Referral, '/referral')
api.add_resource(User, '/user/<string:name_input>')
