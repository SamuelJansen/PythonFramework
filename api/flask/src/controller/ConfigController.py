from flask_restful import Resource
from globals import GlobalsResource

@GlobalsResource(path = '/config')
class GlobalsController(Resource):

    def get(self):
        return {
            'config' : self.api.globals.settingTree,
            'api_tree' : self.api.globals.apiTree
        }

    def post(self):
        pass
