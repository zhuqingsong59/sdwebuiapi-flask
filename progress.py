import config
from flask import request
from flask_restful import Resource


class Progress(Resource):
    def post(self):
        taskId = request.json['taskId']
        print(taskId)
        if (config.sdProgress.get(taskId) == None):
            return {
                'data': 'isWating',
                'code': 0
            }
        print('config.sdProgress:=======================',
              config.sdProgress[taskId]['progress'])
        return {
            'data': config.sdProgress[taskId],
            'code': 0
        }
