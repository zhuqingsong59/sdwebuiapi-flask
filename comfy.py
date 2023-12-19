import time
import json
import base64
from io import BytesIO
from flask import request
from flask_restful import Resource
from PIL import Image, PngImagePlugin
from urllib import request as urlRequest


def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = urlRequest.Request("http://127.0.0.1:8188/prompt", data=data)
    urlRequest.urlopen(req)


class Comfy(Resource):
    def post(self):
        request_json = request.json
        print(request_json)
        taskId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        with open("workflow_api.json", "r") as read_file:
            prompt = json.load(read_file)
            prompt["6"]["inputs"]["text"] = "masterpiece best quality girl"

            prompt["3"]["inputs"]["seed"] = 1

            queue_prompt(prompt)
            return {
                'data': taskId,
                'code': 0
            }
