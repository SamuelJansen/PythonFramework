from flask import Flask
from flask_restful import Api
from globals import Globals
import ResourceService, HomeResource

application = Flask(__name__)
api = Api(application)
Globals.addTo(api)
ResourceService.addTo(api)
