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
        executor.submit(saveImageRun, request_json, taskId)
        return {
            'data': taskId,
            'code': 0
        }


def saveImageRun(request_json, taskId):
    asyncio.run(saveImage(request_json, taskId))


async def saveImage(jsonData, taskId):
    task = config.sdApi.txt2img(**jsonData, use_async=True)
    while not task.done():
        config.sdProgress[taskId] = config.sdApi.get_progress()
        print('in saveImage loop', config.sdProgress[taskId]['progress'])
        await asyncio.sleep(2)
    result = await task
    result.image.save('./static/' + taskId + '.jpeg')
    config.sdProgress[taskId] = {
        'progress': 1,
        'url': 'http://192.168.50.156:7787/static/' + taskId + '.jpeg'
    }
