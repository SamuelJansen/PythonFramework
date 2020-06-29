from flask_restful import Resource
import Globals, UrlResource

@Globals.Resource(path='/')
class HomeResource(Resource):

    def get(self):
        return {'status' : 'UP'}
