from flask_restful import Resource
from globals import GlobalsResource
import Session

@GlobalsResource(path = '/sessions')
class SessionController(Resource):

    def get(self):
        sessionList = self.api.repository.findAllAndCommit(Session)
        return {'sesions' : sessionList}
