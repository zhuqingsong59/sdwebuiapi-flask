from flask import Flask
from txt2img import Txt2img
from img2img import Img2img
from pngInfo import PngInfo
from testApi import TestApi
from progress import Progress
from flask_restful import Api
from getLoras import GetLoras
from translate import Translate
from sdModels import GetModelsNames, GetCurrentModel, SetCurrentModel
from controlnet import CheckControlnet
import config

app = Flask(__name__)
api = Api(app)

api.add_resource(TestApi, '/testApi')
api.add_resource(Txt2img, '/txt2img')
api.add_resource(Img2img, '/img2img')
api.add_resource(Progress, '/progress')
api.add_resource(PngInfo, '/pngInfo')
api.add_resource(Translate, '/translate')
api.add_resource(GetLoras, '/getLoras')
api.add_resource(GetModelsNames, '/getModelsNames')
api.add_resource(GetCurrentModel, '/getCurrentModel')
api.add_resource(SetCurrentModel, '/setCurrentModel')
api.add_resource(CheckControlnet, '/checkControlnet')


if __name__ == '__main__':
    app.run(debug=True, host=config.host, port=config.port)
