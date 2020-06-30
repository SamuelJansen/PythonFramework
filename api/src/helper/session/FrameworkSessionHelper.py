import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def activateSession(self,session):
    session.status = FrameworkStatus[FrameworkConstant.ACTIVE]
    self.session = self.repository.saveAndCommit(session)

def deactivateSessionList(self,sessionList):
    for session in sessionList :
        session.status = FrameworkStatus[FrameworkConstant.INACTIVE]
    self.repository.saveAllAndCommit(sessionList)
