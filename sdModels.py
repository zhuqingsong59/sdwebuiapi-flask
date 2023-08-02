import config
from flask import request
from flask_restful import Resource


class GetModelsNames(Resource):
    def post(self):
        result = config.sdApi.util_get_model_names()
        return {
            'data': result,
            'code': 0
        }


class GetCurrentModel(Resource):
    def post(self):
        result = config.sdApi.util_get_current_model()
        return {
            'data': result,
            'code': 0
        }


class SetCurrentModel(Resource):
    def post(self):
        json_data = request.json
        result = config.sdApi.util_set_model(json_data['modelName'])
        return {
            'data': result,
            'code': 0
        }
