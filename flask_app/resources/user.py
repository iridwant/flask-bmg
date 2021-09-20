from flask.helpers import make_response
from flask.json import jsonify
from flask_jwt_extended.utils import get_jwt_identity
from flask_restx import Resource, reqparse, fields
from flask_jwt_extended import jwt_required
from flask_app.models.user import User as UserModel
from flask_app import bcrpyt, db, api
import re

resource_fields = api.model('User', {
    'email': fields.String('demouser@mail.com'),
    'name': fields.String('Tyler Oakley'),
    'old_password': fields.String('password'),
    'new_password': fields.String('newpassword')
})

class User(Resource):
    req_args = reqparse.RequestParser()
    req_args.add_argument('new_password', type=str, required=True, help='Please input your new password')
    req_args.add_argument('old_password', type=str, required=True, help='Please input your old password')
    req_args.add_argument('email', type=str, required=True, help='Please input your email')
    req_args.add_argument('name', type=str, required=True, help='Please input your name')

    def validate_password(self):
        args = self.req_args.parse_args()
        if len(args.new_password) < 8:
            return False
        return True

    def validate_email(self):
        args = self.req_args.parse_args()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, args.email):
            return False
        return True

    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, name_input):
        query = UserModel.query.filter(UserModel.name.like(f'%{name_input}%')).all()
        if query:
            result = [{'id':i.id, 'username':i.username, 'name':i.name, 'referral_code':i.referral_code} for i in query]
            return make_response(jsonify({'data':result, 'message':'Success get registered user!'}), 200)
        else:
            return make_response(jsonify({'data':[], 'message':'Registered user not found'}), 404)

    @jwt_required()
    @api.expect(resource_fields)
    @api.doc(security='Bearer Auth')
    def put(self, name_input):
        args = self.req_args.parse_args()
        current_user = get_jwt_identity()
        if self.validate_password():
            query = UserModel.query.filter_by(email=args.email).first()
            if query:
                return make_response(jsonify({'message':'Email has been registered! Please pick another one.'}), 400)
            else:
                if self.validate_email():
                    user = UserModel.query.filter(UserModel.name.like(f'%{name_input}%')).filter_by(id=current_user).first()
                    if user:
                        check_old_password = bcrpyt.check_password_hash(user.password, args.old_password)
                        if check_old_password:
                            user.password = bcrpyt.generate_password_hash(args.new_password, 10).decode('utf8')
                            db.session.add(user)
                            db.session.commit()
                            return make_response(jsonify({'message':'Your data has been updated!'}), 200)
                        else:
                            return make_response(jsonify({'message':'Old password does not match!'}), 400)
                    else:
                        return make_response(jsonify({'message':'Name not found! Please recheck!'}), 404)
                else:
                    return make_response(jsonify({'message':'Invalid email address!'}), 400)
        else:
            return make_response(jsonify({'message':'Password length must be 8 characters minimum.'}), 400)
