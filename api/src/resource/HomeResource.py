from flask_restful import Resource
from globals import GlobalsResource
import UrlResource

@GlobalsResource(path = UrlResource.HOME)
class HomeResource(Resource):

    def get(self):
        return {'status' : 'UP'}
