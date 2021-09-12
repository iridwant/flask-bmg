from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask import make_response, jsonify
from flask_app.models.user import User

class Referral(Resource):
    req_args = reqparse.RequestParser()
    req_args.add_argument('referral', type=str, required=True)

    @jwt_required()
    def post(self):
        args = self.req_args.parse_args()
        query = User.query.filter_by(referral_code=args.referral).first()
        if query:
            return make_response(jsonify({'message':'Referral code valid', 'referral_from': query.username}), 200)
        else:
            return make_response(jsonify({'message':'Invalid referral code!'}), 400)
