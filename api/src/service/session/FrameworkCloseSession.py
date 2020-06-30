import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def closeSession(self,commandList):
    if len(commandList) > self._0_ARGUMENT :
        sessionKey = commandList[self._0_ARGUMENT]
    else :
        sessionKey = self.session.key
    session = self.repository.findByKeyAndCommit(sessionKey,Session)
    session.status = FrameworkStatus[FrameworkConstant.INACTIVE]
    self.repository.saveAndCommit(session)
    self.printSuccess(f'"{sessionKey}" session closed successfully')
