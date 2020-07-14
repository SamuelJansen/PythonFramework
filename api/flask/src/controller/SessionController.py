from flask_restful import Resource
from globals import GlobalsResource
import Session
import json

@GlobalsResource(path = '/sessions')
class SessionController(Resource):

    def get(self):
        sessionList = self.api.repository.findAllAndCommit(Session.Session)
        return {'sesions' : json.loads(json.dumps(str(sessionList)))}
