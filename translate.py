import requests
from flask import request
from flask_restful import Resource


class Translate(Resource):
    def post(self):
        request_json = request.json
        textList = request_json['textList']
        print(textList)
        response = requests.post(
            'http://127.0.0.1:7860/physton_prompt/translates', json={
                'api': 'baidu_free',
                'from_lang': 'zh_CN',
                'to_lang': 'en_US',
                'api_config': {},
                'texts': textList
            })
        return {
            'data': response.json(),
            'code': 0
        }
