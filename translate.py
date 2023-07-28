import requests
from flask import request
from flask_restful import Resource


class Translate(Resource):
    def post(self):
        request_json = request.json
        textList = request_json['text'].split('，')
        response = requests()
        print(textList)
        return {
            'data': 2333,
            'code': 0
        }
