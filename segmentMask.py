import cv2
import time
import base64
from PIL import Image
from io import BytesIO
from flask import request
from flask_restful import Resource
from segmentAnythingLib.segment_anything import sam_model_registry, SamAutomaticMaskGenerator


def resize_image(input_image, output_path, max_size=1024):
    original_image = Image.open(input_image)
    width, height = original_image.size

    # 检查图片的宽度和高度是否超过最大值
    if width > max_size or height > max_size:
        # 计算缩放比例
        scale = min(max_size / width, max_size / height)
        # 计算新的宽度和高度
        new_width = int(width * scale)
        new_height = int(height * scale)
        # 调整图片大小
        resized_image = original_image.resize(
            (new_width, new_height), Image.ANTIALIAS)
    else:
        resized_image = original_image
    resized_image.save(output_path)
    return resized_image


class SegmentMask(Resource):
    def post(self):
        request_json = request.json
        currentTime = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        sourcePath = './static/source/' + currentTime + '.png'
        image = resize_image(BytesIO(base64.b64decode(
            request_json['image'].split(',')[1])), sourcePath)

        image = cv2.imread(sourcePath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        sam_checkpoint = "./model/sam_vit_h_4b8939.pth"
        model_type = "vit_h"
        # device = "cuda"
        device = "cpu"

        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)

        mask_generator = SamAutomaticMaskGenerator(
            sam, output_mode="uncompressed_rle")
        masks = mask_generator.generate(image)
        return {
            'data': {
                'image': sourcePath[1:],
                'masks': masks
            },
            'code': 0
        }
