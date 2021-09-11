from flask import jsonify, make_response
from flask_restx import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_app.models.user import User
from flask_app import bcrpyt

class Login(Resource):
    req_args = reqparse.RequestParser()
    req_args.add_argument('username', type=str, required=True, help='Username cannot be empty, please insert your username!')
    req_args.add_argument('password', type=str, required=True, help='Password cannot be empty, please input your password!')

    def post(self):
        args = self.req_args.parse_args()
        query = User.query.filter_by(username=args.username).first()
        if query:
            check_password = bcrpyt.check_password_hash(query.password, args.password)
            if check_password:
                access_token = create_access_token(identity=query.id)
                return make_response(jsonify({
                        'access_token': access_token,
                        'username': args.username,
                        'message': 'Login Successful!'
                    }), 200)
            else:
                return make_response(jsonify({'message': 'Invalid username/password'}), 401)
        else:
            return make_response(jsonify({'message': 'Username not found. Please register first!'}), 401)