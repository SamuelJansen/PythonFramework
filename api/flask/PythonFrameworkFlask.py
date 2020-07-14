from flask import Flask
from flask_restful import Api
import ResourceService

app = Flask(__name__)
api = Api(app)
ResourceService.addApiResourcesTo(api)
