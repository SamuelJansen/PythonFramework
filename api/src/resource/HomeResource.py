from flask_restful import Resource
from globals import Globals
import UrlResource

@Globals.Resource(path = UrlResource.HOME)
class HomeResource(Resource):

    def get(self):
        return {'status' : 'UP'}
