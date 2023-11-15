from flask import Flask, render_template, send_from_directory
from txt2img import Txt2img
from img2img import Img2img
from pngInfo import PngInfo
from testApi import TestApi
from progress import Progress
from flask_restful import Api
from getLoras import GetLoras
from translate import Translate
from sdModels import GetModelsNames, GetCurrentModel, SetCurrentModel
from controlnet import GetModelList, GetModuleList, GetDetect
from inpaint import Segment, Mask
from segmentAnything import SegmentAnything
import config

app = Flask(__name__)


@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('templates', path)


@app.route('/')
def index():
    return render_template('index.html')


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
api.add_resource(GetModelList, '/getModelList')
api.add_resource(GetModuleList, '/getModuleList')
api.add_resource(GetDetect, '/getDetect')
api.add_resource(Segment, '/segment')
api.add_resource(SegmentAnything, '/segmentAnything')
api.add_resource(Mask, '/mask')


if __name__ == '__main__':
    app.config['WERKZEUG_WATCHDOG_IGNORE_DIRECTORIES'] = [
        '/static',
        '/templates'
    ]
    app.run(debug=True, host=config.host, port=config.port)
