from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, APPLICATION_TOKEN, IMPORT_SCRITP_FILE_NAME
import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def addToSession(self,commandList):
    globals = self.globals
    sessionKey, apiKey, apiClassName, gitUrl = getCredentials(self,commandList)
    session = getSession(self,sessionKey)
    if apiKey and apiClassName and gitUrl :
        try :
            importApplicationScript = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
            if self.repository.existsByKey(apiKey,Api) :
                api = self.repository.findByKey(apiKey,Api)
                if api not in session.api_list :
                    session.api_list.append(api)
                    self.repository.saveAll(session.api_list)
                    self.printSuccess(f'"{api.key}" : "{api.class_name}" added successfully')
                globals.debug(f'{globals.TAB}{globals.WARNING}"{api.key}" : "{api.class_name}" already belongs to "{session.key}" session')
            else :
                newApi = Api(apiKey,apiClassName,gitUrl,importApplicationScript,[session])
                newApi = self.repository.save(newApi)
                self.printSuccess(f'"{newApi.key}" : "{newApi.class_name}" added successfully')
            return
        except Exception as exception :
            errorMessage = str(exception)
    else :
        errorMessage = 'failed to parse parameters'
    globals.error(self.__class__, f'failed to add api due {commandList} command list', errorMessage)

def getCredentials(self,commandList) :
    apiKey = apiClassName = gitUrl = None
    try :
        sessionKey = commandList[self._0_ARGUMENT]
        apiKey = commandList[self._1_ARGUMENT]
        apiClassName = commandList[self._2_ARGUMENT]
        if len(commandList[self._3_ARGUMENT:]) > self._3_ARGUMENT :
            gitUrl = commandList[self._3_ARGUMENT]
        else :
            gitUrl = f'''{self.gitCommitter.gitUrl}{apiClassName}.{self.gitCommitter.gitExtension}'''
        return sessionKey, apiKey, apiClassName, gitUrl
    except Exception as exception :
        self.printError(f'''{self.__class__.__name__} error handling commandList "{commandList}". Cause: {str(exception)}''')

def getSession(self,sessionKey) :
    globals = self.globals
    if self.repository.existsByKey(sessionKey,Session) :
        globals.debug(f'{globals.TAB}{globals.WARNING}"{sessionKey}" session key already exists')
        return self.repository.findByKey(sessionKey,Session)
    else :
        newSession = Session(sessionKey,FrameworkStatus[FrameworkConstant.INACTIVE],[])
        return self.repository.save(newSession)
