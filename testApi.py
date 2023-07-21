from flask_restful import Resource


class TestApi(Resource):
    def post(self):
        dic = {
            "a": 1
        }
        return {
            'data': {
                'info': dic
            },
            'code': 0
        }
