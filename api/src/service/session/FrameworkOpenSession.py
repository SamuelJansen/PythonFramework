import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkSessionHelper
import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def openSession(self,commandList) :
    globals = self.globals
    activeSessionList = self.repository.findAllAndCommit(Session)
    sessionKey = commandList[self._0_ARGUMENT]
    if self.repository.existsByKeyAndCommit(sessionKey,Session) :
        FrameworkSessionHelper.deactivateSessionList(self,activeSessionList)
        FrameworkSessionHelper.activateSession(self,self.repository.findByKeyAndCommit(sessionKey,Session))
        self.printSuccess(f'"{sessionKey}" session oppened successfully')
    else :
        self.printError(f'"{sessionKey}" session not found')
        self.session = None
