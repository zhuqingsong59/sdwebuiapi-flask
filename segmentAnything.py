import cv2
import time
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from flask import request
from flask_restful import Resource
from segmentAnythingLib.segment_anything import sam_model_registry, SamPredictor


class SegmentAnything(Resource):
    def post(self):
        request_json = request.json
        currentTime = time.strftime(
            '%Y%m%d%H%M%S', time.localtime(time.time()))
        image = Image.open(
            BytesIO(base64.b64decode(request_json['image'].split(',')[1])))
        imagePath = './static/segment/' + currentTime + '.png'
        image.save(imagePath)
        checkpoint = './model/sam_vit_h_4b8939.pth'
        model_type = "vit_h"
        sam = sam_model_registry[model_type](checkpoint=checkpoint)
        sam.to(device='cpu')
        predictor = SamPredictor(sam)
        image = cv2.imread(imagePath)
        predictor.set_image(image)
        image_embedding = predictor.get_image_embedding().cpu().numpy()
        embeddingPath = './static/npy/' + currentTime + '.npy'
        np.save(embeddingPath, image_embedding)
        return {
            'data': {
                'embedding': embeddingPath[1:],
                'image': imagePath[1:],
                'model': '/static/onnx/vit_h.onnx'
            },
            'code': 0
        }
