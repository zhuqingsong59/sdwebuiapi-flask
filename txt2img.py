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
        executor.submit(self.txt2img, request_json, taskId)
        return {
            'data': taskId,
            'code': 0
        }

    def txt2img(self, txt2imgParams, taskId):
        result = config.sdApi.txt2img(**txt2imgParams)
        index = 0
        fileNameList = []
        for image in result.images:
            fileName = taskId + '_' + str(index) + '.jpeg'
            image.save(fileName)
            fileNameList.append(fileName)
            index = index + 1
        config.sdProgress[taskId] = {
            'progress': 1,
            'urlList': list(map(lambda item: '/static/' + item, fileNameList))
        }

    #  异步调用生成函数
    def startTxt2img(self, txt2imgParams, taskId):
        asyncio.run(self.txt2imgAsync(txt2imgParams, taskId))

    # 调用api生成图片，并记录生成进度
    async def txt2imgAsync(self, txt2imgParams, taskId):
        task = config.sdApi.txt2img(**txt2imgParams, use_async=True)
        while not task.done():
            config.sdProgress[taskId] = config.sdApi.get_progress()
            await asyncio.sleep(2)
        result = await task
        index = 0
        fileNameList = []
        for image in result.images:
            fileName = './static/' + taskId + '_' + str(index) + '.jpeg'
            image.save(fileName)
            fileNameList.append(fileName)
            index = index + 1
        config.sdProgress[taskId] = {
            'progress': 1,
            'urlList': list(map(lambda item: '/static/' + item, fileNameList))
        }
