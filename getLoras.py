import config
from flask_restful import Resource


class GetLoras(Resource):
    def post(self):
        result = config.sdApi.get_loras()
        return {
            'data': result,
            'code': 0
        }
