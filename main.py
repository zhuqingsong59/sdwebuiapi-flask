from flask import Flask
from flask_restful import Api
from progress import Progress
from txt2img import Txt2img

app = Flask(__name__)
api = Api(app)


api.add_resource(Txt2img, '/sdapi/v1/txt2img')
api.add_resource(Progress, '/sdapi/v1/progress')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='7787')
