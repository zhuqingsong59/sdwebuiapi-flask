from flask import Flask
from flask_restful import Api
from progress import Progress
from txt2img import Txt2img
from img2img import Img2img
from pngInfo import PngInfo
import config

app = Flask(__name__)
api = Api(app)


api.add_resource(Txt2img, '/txt2img')
api.add_resource(Img2img, '/img2img')
api.add_resource(Progress, '/progress')
api.add_resource(PngInfo, '/pngInfo')


if __name__ == '__main__':
    app.run(debug=True, host=config.host, port=config.port)
