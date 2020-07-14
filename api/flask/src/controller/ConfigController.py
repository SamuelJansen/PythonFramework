import flask_restful
from globals import GlobalsResource

@GlobalsResource(path = '/config')
class ConfigController(flask_restful.Resource):

    def get(self):
        return {
            'config' : self.api.globals.settingTree,
            'api_tree' : self.api.globals.apiTree
        }

    def post(self):
        pass
