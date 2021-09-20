from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_app import config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI

db = SQLAlchemy(app)
bcrpyt = Bcrypt(app)
migrate = Migrate(app, db)
api = Api(app, version='1.0.0', title='API BMG', description='API for BMG technical test', security='Bearer Auth', authorizations=config.AUTHORIZATIONS)
jwt = JWTManager(app)
cache = Cache(app, config={'CACHE_TYPE':'redis', 'CACHE_REDIS_URL':config.REDIS_URL})

@app.before_first_request
def create_app():
    db.create_all()
    db.session.commit()

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
