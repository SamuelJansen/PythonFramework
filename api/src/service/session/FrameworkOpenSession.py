import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkSessionHelper
import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def openSession(self,commandList) :
    globals = self.globals
    activeSessionList = self.repository.findAll(Session)
    sessionKey = commandList[self._0_ARGUMENT]
    if self.repository.existsByKey(sessionKey,Session) :
        FrameworkSessionHelper.deactivateSessionList(self,activeSessionList)
        FrameworkSessionHelper.activateSession(self,self.repository.findByKey(sessionKey,Session))
        self.printSuccess(f'"{sessionKey}" session oppened successfully')
    else :
        self.printError(f'"{sessionKey}" session not found')
        self.session = None
