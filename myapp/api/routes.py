from flask import Blueprint
from flask_restplus import Api, Resource

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')

languages = []

@api.route('/languages')
class Languages(Resource):
    def get(self):
        return {'hey': 'threr'}
