import config
from flask import request
from flask_restful import Resource


class Progress(Resource):
    def post(self):
        taskId = request.json['taskId']
        if (config.sdProgress.get(taskId) == None):
            return {
                'data': 'isWating',
                'code': 0
            }
        return {
            'data': config.sdProgress[taskId],
            'code': 0
        }
