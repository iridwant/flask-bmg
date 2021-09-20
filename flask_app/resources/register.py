from flask_app import bcrpyt, db
from flask_app.models.user import User
from flask import jsonify, make_response
from flask_restx import Resource, reqparse, fields
from flask_app import api
import uuid
import re

resource_fields = api.model('Register', {
    'username': fields.String('demouser'),
    'password': fields.String('password'),
    'email': fields.String('demouser@mail.com'),
    'name': fields.String('Tyler Oakley'),
})

class Register(Resource):
    req_args = reqparse.RequestParser()
    req_args.add_argument('username', type=str, required=True, help='Please input your username', default='demouser')
    req_args.add_argument('password', type=str, required=True, help='Please input your password', default='password')
    req_args.add_argument('email', type=str, required=True, help='Please input your email', default='demouser@mail.com')
    req_args.add_argument('name', type=str, required=True, help='Please input your name', default='Tyler Oakley')
    req_args.add_argument('referral', type=str)

    def validate_username_password(self):
        args = self.req_args.parse_args()
        if len(args.username) < 8 or len(args.password) < 8:
            return False
        return True

    def validate_email(self):
        args = self.req_args.parse_args()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, args.email):
            return False
        return True

    @api.expect(resource_fields)
    @api.doc(security=None)
    def post(self):
        args = self.req_args.parse_args()
        
        if not self.validate_email():
            return make_response(jsonify({'message': 'Invalid email address!'}), 400)
        if not self.validate_username_password():
            return make_response(jsonify({'message': 'Username/password length must be minimum of 8 characters!'}), 400)
        
        hashed = bcrpyt.generate_password_hash(args.password, 10).decode('utf8')
        new_user = {
            'username': args.username,
            'password': hashed,
            'email': args.email,
            'name': args.name,
            'referral_code': args.referral if args.referral is not None and args.referral else str(uuid.uuid4()).upper()[:5]
        }
        user = User(**new_user)
        try:
            db.session.add(user)
            db.session.commit()
            return make_response(jsonify({
                    'message': 'User created!',
                    'data': {
                        'username': new_user['username'],
                        'email': new_user['email'],
                        'referral_code': new_user['referral_code']
                    }
                }), 201)
        except:
            return make_response(jsonify({'message': 'Username/email already registered. Please pick another one!'}), 400)
                
