from flask_restful import Resource
import globals
import UrlResource

@globals.Resource(path = UrlResource.HOME)
class HomeResource(Resource):

    def get(self):
        return {'status' : 'UP'}
