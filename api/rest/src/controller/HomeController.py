import flask_restful
from globals import GlobalsResource

@GlobalsResource(path = '/')
class HomeController(flask_restful.Resource):

    def get(self):
        return {'status' : 'UP'}
