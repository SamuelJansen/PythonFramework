import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def newSession(self,commandList) :
    sessionKey = commandList[self._0_ARGUMENT]
    if self.repository.existsByKey(sessionKey,Session) :
        self.printError(f'{sessionKey} already exists')
    else :
        self.repository.saveNew(sessionKey,FrameworkStatus[FrameworkConstant.INACTIVE],[],Session)
        self.printSuccess(f'{sessionKey} created successfully')
