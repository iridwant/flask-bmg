from flask.helpers import make_response
from flask.json import jsonify
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from flask_app import cache
import requests

class Hero(Resource):
    @jwt_required()
    def get(self, name):
        url = 'https://ddragon.leagueoflegends.com/cdn/6.24.1/data/en_US/champion.json'

        response = requests.get(url)
        if response.status_code == 200:
            hero_cache = cache.get('hero_data')
            if hero_cache:    
                hero_list = [value for key, value in hero_cache.items() if name in key]
            else:
                hero_data = response.json()['data']
                cache.set('hero_data', hero_data)
                hero_list = [value for key, value in hero_data.items() if name in key]
            
            if hero_list:
                return make_response(jsonify({'message':'Success get hero data!', 'total_data':len(hero_list), 'data':hero_list}), 200)
            else:
                return make_response(jsonify({'message':'Hero data not found!', 'total_data':len(hero_list), 'data':hero_list}), 404)
        else:
            return make_response(jsonify({"message": "Server is currently down"}), 500)