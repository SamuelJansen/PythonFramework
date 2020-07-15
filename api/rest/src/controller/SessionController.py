import flask_restful
from globals import GlobalsResource
import Session
import json

@GlobalsResource(path = '/sessions')
class SessionController(flask_restful.Resource):

    def get(self):
        sessionList = self.api.repository.findAllAndCommit(Session.Session)
        return {'sesions' : json.loads(json.dumps(str(sessionList)))}
