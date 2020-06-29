from flask import Flask
from flask_restful import Api
import ResourceService, HomeResource, Globals

application = Flask(__name__)
api = Api(application)
Globals.addTo(api)
ResourceService.addTo(api)
