from flask import Flask
from flask_restful import Api
import globals
import ResourceService, HomeResource

application = Flask(__name__)
api = Api(application)
globals.addTo(api)
ResourceService.addTo(api)
