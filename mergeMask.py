import time
from PIL import Image
from flask import request
from flask_restful import Resource
from utils import base64_to_img, pil_to_base64


class MergeMask(Resource):
    def post(self):
        request_json = request.json

        maskList = request_json['mask_list']
        output_path = './static/outputs/' + \
            time.strftime('%Y%m%d%H%M%S', time.localtime(
                time.time())) + '_mask.png'

        base_mask = Image.open(base64_to_img(maskList[0])).convert('RGBA')
        for mask_file in maskList[1:]:
            mask = Image.open(base64_to_img(mask_file)).convert('RGBA')
            assert mask.size == base_mask.size, "所有图片的大小需要相同"

            base_mask = Image.alpha_composite(base_mask, mask)
        base_mask.save(output_path)

        return {
            'data': 'data:image/png;base64,' + pil_to_base64(base_mask),
            'code': 0
        }
