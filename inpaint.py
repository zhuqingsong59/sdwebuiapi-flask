import time
import base64
import importlib
import numpy as np
from io import BytesIO
from flask import request
from PIL import Image, ImageDraw
from flask_restful import Resource

inpalib = importlib.import_module("inpaint-anything.inpalib")


class Segment(Resource):
    def post(self):
        request_json = request.json
        use_sam_id = "sam_hq_vit_b.pth"
        input_image = np.array(Image.open(
            BytesIO(base64.b64decode(request_json['images'].split(',')[1]))))
        sam_masks = inpalib.generate_sam_masks(
            input_image, use_sam_id, anime_style_chk=False)
        sam_masks = inpalib.sort_masks_by_area(sam_masks)
        seg_color_image = inpalib.create_seg_color_image(
            input_image, sam_masks)
        currentTime = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        Image.fromarray(seg_color_image).save(
            './static/outputs/segment/' + currentTime + '.png')
        return {
            'data': '/static/outputs/segment/' + currentTime + '.png',
            'code': 0
        }


class Mask(Resource):
    def post(self):
        request_json = request.json
        use_sam_id = "sam_hq_vit_b.pth"
        input_image = np.array(Image.open(
            BytesIO(base64.b64decode(request_json['images'].split(',')[1]))))
        sam_masks = inpalib.generate_sam_masks(
            input_image, use_sam_id, anime_style_chk=False)
        sam_masks = inpalib.sort_masks_by_area(sam_masks)

        sketch_image = Image.open(
            BytesIO(base64.b64decode(request_json['sketch_image'].split(',')[1])))

        mask_image = inpalib.create_mask_image(
            np.array(sketch_image), sam_masks, ignore_black_chk=True)
        currentTime = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        Image.fromarray(mask_image).save(
            './static/mask/' + currentTime + '.png')
        return {
            'data': '/static/mask/' + currentTime + '.png',
            'code': 0
        }
