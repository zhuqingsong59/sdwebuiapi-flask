import json
import config
import base64
from PIL import Image
from io import BytesIO
from flask import request
from flask_restful import Resource
from sdwebuiFn import parse_generation_parameters


class PngInfo(Resource):
    def post(self):
        request_json = request.json
        image = Image.open(
            BytesIO(base64.b64decode(request_json['images'].split(',')[1])))
        result = config.sdApi.png_info(image)
        return {
            'data': {
                'info': parse_generation_parameters(result.info),
                'parameters': result.parameters
            },
            'code': 0
        }
