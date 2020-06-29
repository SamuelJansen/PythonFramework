import Api, Session, FrameworkConstant
from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, APPLICATION_TOKEN
FrameworkStatus = FrameworkConstant.Status
Session = Session.Session
Api = Api.Api

def getBasicSession(self):
    basicSession = getBasicSession(self)
    return self.repository.save(basicSession)

def getBasicSession(self) :
    basicSessionKey = self.globals.getApiSetting('api.basic.session.key')
    if self.repository.existsByKey(basicSessionKey,Session) :
        return self.repository.findByKey(basicSessionKey,Session)
    else :
        apiList = getDefaultApiList(self)
        return self.repository.save(Session(basicSessionKey,FrameworkConstant.ACTIVE,apiList))

def getDefaultApiList(self) :
    apiKey = self.globals.getApiSetting('api.basic.api.key')
    if (self.repository.existsByKey(apiKey,Api)) :
        return [self.repository.findByKey(apiKey,Api)]
    else :
        apiClassName = self.globals.getApiSetting('api.basic.api.class-name')
        gitUrl = self.globals.getApiSetting('api.git.url')
        gitExtension = self.globals.getApiSetting('api.git.extension')
        importScript = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
        sessionList = []
        return [Api(apiKey,apiClassName,f'''{gitUrl}/{apiClassName}.{gitExtension}''',importScript,sessionList)]
