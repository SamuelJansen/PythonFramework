from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, PROJECT_TOKEN, APPLICATION_TOKEN, IMPORT_SCRITP_FILE_NAME
import Api, Session
Api = Api.Api
Session = Session.Session
from python_helper import log

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def addToSession(self,commandList):
    globals = self.globals
    sessionKey, apiKey, apiProjectName, apiClassName, gitUrl = getCredentials(self,commandList)
    session = getSession(self,sessionKey)
    if apiKey and apiProjectName and apiClassName and gitUrl :
        try :
            importApplicationScript = ADD_APPLICATION_FILE_SCRIPT.replace(PROJECT_TOKEN,apiProjectName)
            importApplicationScript = importApplicationScript.replace(APPLICATION_TOKEN,apiClassName)
            if self.repository.existsByKeyAndCommit(apiKey,Api) :
                api = self.repository.findByKeyAndCommit(apiKey,Api)
                if api not in session.apiList :
                    session.apiList.append(api)
                    self.repository.saveAllAndCommit(session.apiList)
                    self.printSuccess(f'"{api.key}" : "{api.className}" added successfully')
                else :
                    self.printWarning(f'"{api.key}" : "{api.className}" api already belongs to "{session.key}" session')
            else :
                newApi = Api(apiKey,apiProjectName,apiClassName,gitUrl,importApplicationScript,[session])
                newApi = self.repository.saveAndCommit(newApi)
                self.printSuccess(f'"{newApi.key}" : "{newApi.className}" added successfully')
            return
        except Exception as exception :
            errorMessage = str(exception)
    else :
        errorMessage = 'failed to parse parameters'
    log.error(self.__class__, f'failed to add api due {commandList} command list', errorMessage)

def getCredentials(self,commandList) :
    apiKey = apiClassName = gitUrl = None
    try :
        sessionKey = commandList[self._0_ARGUMENT]
        apiKey = commandList[self._1_ARGUMENT]
        apiProjectName = commandList[self._2_ARGUMENT]
        apiClassName = commandList[self._3_ARGUMENT]
        if len(commandList[self._4_ARGUMENT:]) >= 1 :
            gitUrl = commandList[self._4_ARGUMENT]
        else :
            gitUrl = f'''{self.gitCommitter.gitUrl}{apiProjectName}.{self.gitCommitter.gitExtension}'''
        return sessionKey, apiKey, apiProjectName, apiClassName, gitUrl
    except Exception as exception :
        self.printError(f'''{self.__class__.__name__} error handling commandList "{commandList}". Cause: {str(exception)}''')

def getSession(self,sessionKey) :
    if self.repository.existsByKeyAndCommit(sessionKey,Session) :
        self.printWarning(f'"{sessionKey}" session key already exists')
        return self.repository.findByKeyAndCommit(sessionKey,Session)
    else :
        newSession = Session(sessionKey,FrameworkStatus[FrameworkConstant.INACTIVE],[])
        return self.repository.saveAndCommit(newSession)
