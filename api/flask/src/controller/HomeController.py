from flask_restful import Resource
from globals import GlobalsResource

@GlobalsResource(path = '/')
class HomeController(Resource):

    def get(self):
        return {'status' : 'UP'}
