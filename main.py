from flask import Flask
from txt2img import Txt2img
from img2img import Img2img
from pngInfo import PngInfo
from testApi import TestApi
from progress import Progress
from flask_restful import Api
from getLoras import GetLoras
import config

app = Flask(__name__)
api = Api(app)

api.add_resource(TestApi, '/testApi')
api.add_resource(Txt2img, '/txt2img')
api.add_resource(Img2img, '/img2img')
api.add_resource(Progress, '/progress')
api.add_resource(PngInfo, '/pngInfo')
api.add_resource(GetLoras, '/getLoras')


if __name__ == '__main__':
    app.run(debug=True, host=config.host, port=config.port)
