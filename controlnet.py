import config
import base64
from PIL import Image
from io import BytesIO
from flask import request
from flask_restful import Resource


class GetModelList(Resource):
    def post(self):
        result = config.sdApi.controlnet_model_list()
        return {
            'data': result,
            'code': 0
        }


class GetModuleList(Resource):
    def post(self):
        result = config.sdApi.controlnet_module_list()
        return {
            'data': result,
            'code': 0
        }


class GetDetect(Resource):
    def post(self):
        request_json = request.json
        module = request_json['module']
        img = Image.open(
            BytesIO(base64.b64decode(request_json['images'].split(',')[1])))
        result = config.sdApi.controlnet_detect(images=[img], module=module)
        image_data = BytesIO()
        result.image.save(image_data, format='PNG')
        image_data_bytes = image_data.getvalue()
        encoded_image = base64.b64encode(image_data_bytes).decode('utf-8')
        return {
            'data': {
                'image': encoded_image,
                'poses': result.poses
            },
            'code': 0
        }
