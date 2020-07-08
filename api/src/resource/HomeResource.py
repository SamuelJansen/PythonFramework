from flask_restful import Resource
import globals as Globals
import UrlResource

@Globals.Resource(path = UrlResource.HOME)
class HomeResource(Resource):

    def get(self):
        return {'status' : 'UP'}
