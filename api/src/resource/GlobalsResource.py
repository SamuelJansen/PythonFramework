from flask_restful import Resource
import Globals, UrlResource

@Globals.Resource(path='/config')
class GlobalsResource(Resource):

    def get(self):
        return {
            'config' : self.api.globals.settingTree,
            'api_tree' : self.api.globals.apiTree
        }

    def post(self):
        pass
