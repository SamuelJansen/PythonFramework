import Api, Session, FrameworkConstant
from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, APPLICATION_TOKEN
FrameworkStatus = FrameworkConstant.Status
Session = Session.Session
Api = Api.Api

def getBasicSession(self):
    basicSession = getBasicSession(self)
    return self.repository.saveAndCommit(basicSession)

def getBasicSession(self) :
    basicSessionKey = self.globals.getApiSetting('api.basic.session.key')
    if self.repository.existsByKeyAndCommit(basicSessionKey,Session) :
        return self.repository.findByKeyAndCommit(basicSessionKey,Session)
    else :
        apiList = getDefaultApiList(self)
        return self.repository.saveAndCommit(Session(basicSessionKey,FrameworkConstant.ACTIVE,apiList))

def getDefaultApiList(self) :
    apiKey = self.globals.getApiSetting('api.basic.api.key')
    if (self.repository.existsByKeyAndCommit(apiKey,Api)) :
        return [self.repository.findByKeyAndCommit(apiKey,Api)]
    else :
        projectName = self.globals.getApiSetting('api.basic.api.project-name')
        apiClassName = self.globals.getApiSetting('api.basic.api.class-name')
        gitUrl = self.globals.getApiSetting('api.git.url')
        gitExtension = self.globals.getApiSetting('api.git.extension')
        importScript = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
        sessionList = []
        return [Api(apiKey,projectName,apiClassName,f'''{gitUrl}/{apiClassName}.{gitExtension}''',importScript,sessionList)]
