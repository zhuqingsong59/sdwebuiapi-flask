import time
import base64
import config
from PIL import Image
from io import BytesIO
from flask import request
from PIL import PngImagePlugin
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
        img2imgParams['images'][0].save('./cache/' + taskId + '.png')
        if 'mask_image' in img2imgParams:
            # img2imgParams['mask_image'] = Image.open(
            #     BytesIO(base64.b64decode(img2imgParams['mask_image'].split(',')[1])))

            maskImg = Image.open(
                BytesIO(base64.b64decode(img2imgParams['mask_image'].split(',')[1])))
            # # 将图片转换为RGB模式
            maskImg = maskImg.convert('RGB')
            # 遍历每个像素
            for x in range(maskImg.width):
                for y in range(maskImg.height):
                    r, g, b = maskImg.getpixel((x, y))
                    # 如果像素是黑色
                    if r == 0 and g == 0 and b == 0:
                        # 将它变成黑色
                        maskImg.putpixel((x, y), (0, 0, 0))
                    else:
                        # 如果像素是其他颜色，将它变成白色
                        maskImg.putpixel((x, y), (255, 255, 255))
            img2imgParams['mask_image'] = maskImg
            img2imgParams['inpainting_fill'] = 1
            img2imgParams['inpainting_mask_invert'] = 1

            img2imgParams['mask_image'].save(
                './static/mask/' + taskId + '.png')
        if 'controlnet_units' in img2imgParams:
            controlNetUnit = img2imgParams['controlnet_units']
            controlNetUnit['input_image'] = Image.open(
                BytesIO(base64.b64decode(controlNetUnit['input_image'].split(',')[1])))
            unit = config.webuiapi.ControlNetUnit(**controlNetUnit)
            img2imgParams['controlnet_units'] = [unit]
        result = config.sdApi.img2img(**img2imgParams)
        index = 0
        fileNameList = []
        pnginfo_data = PngImagePlugin.PngInfo()
        pnginfo_data.add_text('parameters', ''.join(result.info['infotexts']))
        for image in result.images:
            fileName = taskId + '_' + str(index) + '.png'
            image.save('./static/outputs/img2img/' +
                       fileName, pnginfo=pnginfo_data)
            fileNameList.append(fileName)
            index = index + 1
        config.sdProgress[taskId] = {
            'progress': 1,
            'urlList': list(map(lambda item: '/static/outputs/img2img/' + item, fileNameList))
        }
