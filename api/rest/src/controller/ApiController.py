import flask_restful
from globals import GlobalsResource
import Api
import json

@GlobalsResource(path = '/apis')
class ApiController(flask_restful.Resource):

    def get(self):
        apiList = self.api.repository.findAllAndCommit(Api.Api)
        return {'apis' : json.loads(json.dumps(str(apiList)))}
