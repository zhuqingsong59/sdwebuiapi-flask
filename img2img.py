import time
import base64
import config
from PIL import Image
from io import BytesIO
from flask import request
from flask_restful import Resource
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)


class Img2img(Resource):
    def post(self):
        request_json = request.json
        taskId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        executor.submit(self.img2img, request_json, taskId)
        return {
            'data': taskId,
            'code': 0
        }

    def img2img(self, img2imgParams, taskId):
        img2imgParams['images'] = [Image.open(
            BytesIO(base64.b64decode(img2imgParams['images'].split(',')[1])))]
        img2imgParams['images'][0].save('./cache/' + taskId + '.jpeg')
        result = config.sdApi.img2img(**img2imgParams)
        index = 0
        fileNameList = []
        for image in result.images:
            fileName = taskId + '_' + str(index) + '.jpeg'
            image.save('./static/' + fileName)
            fileNameList.append(fileName)
            index = index + 1
        config.sdProgress[taskId] = {
            'progress': 1,
            'urlList': list(map(lambda item: '/static/' + item, fileNameList))
        }
