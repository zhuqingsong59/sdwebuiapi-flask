import config
from flask import request
from flask_restful import Resource


class CheckControlnet(Resource):
    def post(self):
        result = config.sdApi.controlnet_version()
        print(result)
        return {
            'data': result,
            'code': 0
        }
