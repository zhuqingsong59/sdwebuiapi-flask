import time
import config
import asyncio
from flask import request
from flask_restful import Resource
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(2)


class Txt2img(Resource):
    def post(self):
        request_json = request.json
        taskId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        executor.submit(saveImage, request_json, taskId)
        return {
            'data': taskId,
            'code': 0
        }


def saveImage(jsonData, taskId):
    print('==============saveImage===============', jsonData)
    result = config.sdApi.txt2img(**jsonData)
    result.image.save('./static/' + taskId + '.jpeg')
    index = 0
    print('result.image', result.image)
    print('result.images', result.images)
    for image in result.images:
        print('image', image)
        image.save('./static/' + taskId + '_' + str(index) + '.jpeg')
        index = index + 1
