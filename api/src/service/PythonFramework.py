from PythonFrameworkTable import Model
import SqlAlchemyHelper, GitCommitter
import Api, Session
import FrameworkConstant
from LoadSessionAnnotation import LoadSession
from SessionMethodAnnotation import SessionMethod
from PythonFrameworkApplicationScript import *
import FrameworkNewSession, FrameworkOpenSession, FrameworkPrintSession, FrameworkLoadApiClassSet, FrameworkCloseSession, FrameworkAddToSession
import FrameworkSessionHelper

Api = Api.Api
Session = Session.Session
GitCommitter = GitCommitter.GitCommitter
# SqlAlchemyHelper = SqlAlchemyHelper.SqlAlchemyHelper
FrameworkStatus = FrameworkConstant.Status

class PythonFramework:

    UNEXPECTED_KEYWORD_ARGUMMENT = '__init__() got an unexpected keyword argument'
    MISSING_REQUIRED_ARGUMENT = '__init__() missing 1 required positional argument:'

    API_KEY_FRAMEWORK = 'framework'
    API_KEY_GIT_COMMITTER = 'git-committer'

    _0_API_KEY = 0
    _1_COMMAND = 1
    _0_ARGUMENT = 2
    _1_ARGUMENT = 3
    _2_ARGUMENT = 4
    _3_ARGUMENT = 5

    COMMAND_ADD_API_BY_KEY_VALUE = 'add-api-by-key-value'

    COMMAND_NEW_SESSION = 'new-session'
    COMMAND_OPEN_SESSION = 'open-session'
    COMMAND_ADD_TO_SESSION = 'add-to-session'
    COMMAND_REMOVE_FROM_SESSION = 'remove-from-session'
    COMMAND_SAVE_SESSION = 'save-session'
    COMMAND_PRINT_SESSION = 'print-session'
    COMMAND_SESSION_COMMAND_LIST = 'session-command-list'
    COMMAND_CLOSE_SESSION = 'close-session'

    COMMAND_LIST_ALL_SESSION = 'list-all-session'

    COMMAND_COMMAND_LIST = 'command-list'
    commandList = {
        COMMAND_ADD_API_BY_KEY_VALUE : [],
        COMMAND_NEW_SESSION : [],
        COMMAND_OPEN_SESSION : [],
        COMMAND_ADD_TO_SESSION : ['sessionKey','apiKey','apiClassName','gitUrl'],
        COMMAND_REMOVE_FROM_SESSION : [],
        COMMAND_SAVE_SESSION : [],
        COMMAND_PRINT_SESSION : [],
        COMMAND_SESSION_COMMAND_LIST : [],
        COMMAND_CLOSE_SESSION : [],
        COMMAND_LIST_ALL_SESSION : []
    }

    KW_GIT_COMMITTER = API_KEY_GIT_COMMITTER

    @SessionMethod
    def handleCommandList(self,commandList):
        globals = self.globals
        globals.debug(f'{self.__class__.__name__}.commandList = {commandList}')
        globals.debug(f'session = {self.session}')
        return self.apiSet[commandList[self._0_API_KEY]][commandList[self._1_COMMAND]](commandList)

    @LoadSession
    def handleSystemArgumentValue(self,commandList,externalFunction):
        globals = self.globals
        try :
            if self.apiClassSet :
                apiClass = self.apiClassSet.get(commandList[self._0_API_KEY])
                if apiClass and apiClass in [self.__class__, GitCommitter] :
                    globals.success(self.__class__, f'running {commandList} command list')
                    return self.handleCommandList(commandList)
                elif apiClass :
                    globals.overrideApiTree(apiClass.__name__)
                    api = apiClass(*self.args,**self.kwargs)
                    globals.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                else :
                    globals.failure(self.__class__,'''couldn't instance api class''', globals.NOTHING)
            else :
                globals.debug(f'{commandList[self._0_API_KEY]} key called and running all alone')
                return externalFunction(commandList,globals,**self.kwargs)
        except Exception as exception :
            errorMessage = str(exception)
            if self.MISSING_REQUIRED_ARGUMENT in errorMessage :
                newArgs = *self.args,self.globals
                try :
                    api = apiClass(*newArgs,**self.kwargs)
                    globals.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                except Exception as exception :
                    secondErrorMessage = f', after first try: {str(exception)}'
                    newArgs = *self.args,self.session,self.globals
                    try :
                        api = apiClass(*newArgs,**self.kwargs)
                        globals.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
                        return api.handleCommandList(commandList)
                    except Exception as exception :
                        thirdErrorMessage = f', after second try: {str(exception)}'
            else :
                secondErrorMessage = ''
                thirdErrorMessage = ''
            globals.error(self.__class__, f'error processing "{commandList[self._0_API_KEY]}" call{secondErrorMessage}{thirdErrorMessage}', errorMessage)

    def __init__(self,*args,**kwargs):
        self.globals = args[-1]
        externalFunction = args[-2]
        self.args = args[:-2]
        self.kwargs = kwargs
        self.name = self.globals.getApiSetting('api.name')
        self.repositoryName = self.name
        self.repository = SqlAlchemyHelper.SqlAlchemyHelper(self.repositoryName,model=Model)
        # self.repository.run()
        self.importApplicationScriptPath = f'{self.globals.apiPath}{self.globals.baseApiPath}runtime{self.globals.BACK_SLASH}{IMPORT_SCRITP_FILE_NAME}.{self.globals.PYTHON_EXTENSION}'

        self.apiSet = {}
        self.apiSet[self.API_KEY_FRAMEWORK] = {
            self.COMMAND_ADD_API_BY_KEY_VALUE : self.addApiByKeyValue,

            self.COMMAND_NEW_SESSION : self.newSession,
            self.COMMAND_ADD_TO_SESSION : self.addToSession,
            self.COMMAND_REMOVE_FROM_SESSION : self.removeFromSession,
            self.COMMAND_SAVE_SESSION : self.saveSession,
            self.COMMAND_OPEN_SESSION : self.openSession,
            self.COMMAND_PRINT_SESSION : self.printSession,
            self.COMMAND_SESSION_COMMAND_LIST : self.sessionCommandList,
            self.COMMAND_CLOSE_SESSION : self.closeSession,

            self.COMMAND_LIST_ALL_SESSION : self.listAllSession,

            self.COMMAND_COMMAND_LIST : self.printCommandList
        }
        self.apiClassSet = {
            self.API_KEY_FRAMEWORK : PythonFramework,
            self.API_KEY_GIT_COMMITTER : GitCommitter
        }
        self.gitCommitter = self.getGitCommitter()
        self.apiSet[self.API_KEY_GIT_COMMITTER] = self.gitCommitter.commandSet
        self.loadApiClassSet()

    @LoadSession
    def getGitCommitter(self):
        return GitCommitter(self.session,self.globals)

    @SessionMethod
    def loadApiClassSet(self):
        FrameworkLoadApiClassSet.loadApiClassSet(self)

    @SessionMethod
    def newSession(self,commandList):
        return FrameworkNewSession.newSession(self,commandList)

    @SessionMethod
    def addToSession(self,commandList):
        return FrameworkAddToSession.addToSession(self,commandList)

    @SessionMethod
    def removeFromSession(self,commandList):
        self.globals.debug(f'{self.__class__.__name__}.removeFromSession({commandList})')
        pass

    @SessionMethod
    def saveSession(self,commandList):
        self.globals.debug(f'{self.__class__.__name__}.saveSession({commandList})')
        pass

    @SessionMethod
    def listAllSession(self,commandList):
        self.globals.debug(f'{self.__class__.__name__}.listAllSession({commandList})')
        pass

    @SessionMethod
    def openSession(self,commandList):
        return FrameworkOpenSession.openSession(self,commandList)

    @SessionMethod
    def printSession(self,commandList):
        return FrameworkPrintSession.printSession(self,commandList)

    @SessionMethod
    def sessionCommandList(self,commandList):
        self.globals.printTree(self.apiSet,f'{self.globals.TAB}Command list: ',depth=2)

    @SessionMethod
    def closeSession(self,commandList):
        return FrameworkCloseSession.closeSession(self,commandList)

    @SessionMethod
    def addApiByKeyValue(self,commandList):
        self.globals.debug(f'{self.__class__.__name__}.addApiByKeyValue({commandList})')
        globals = self.globals
        if not self.session :
            sessionKey = globals.NOTHING
            while sessionKey == globals.NOTHING :
                sessionKey = input(f'{globals.TAB}Type session key: ')
                if not sessionKey == globals.NOTHING :
                    if self.repository.existsByKey(sessionKey,Session) :
                        globals.debug(f'{globals.TAB}{globals.WARNING}"{sessionKey}" session key already exists')
                        self.session = self.repository.findByKey(sessionKey,Session)
                    else :
                        newSession = Session(sessionKey,FrameworkStatus[FrameworkConstant.INACTIVE],[])
                        self.session = self.repository.save(newSession)
                    print(f'session = {self.session}')
        apiKey, apiClassName, gitUrl = self.createCredentials(commandList)
        if apiKey and apiClassName and gitUrl :
            try :
                importApplicationScript = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
                if self.repository.existsByKey(apiKey,Api) :
                    api = self.repository.findByKey(apiKey,Api)
                    if api not in self.session.api_list :
                        self.session.api_list.append(api)
                        self.repository.saveAll(self.session.api_list)
                        self.printSuccess(f'"{api.key}" : "{api.class_name}" added successfully')
                    globals.debug(f'{globals.TAB}{globals.WARNING}"{api.key}" : "{api.class_name}" already belongs to "{self.session.key}" session')
                else :
                    newApi = Api(apiKey,apiClassName,gitUrl,importApplicationScript,[self.session])
                    print(f'newApi = {newApi}')
                    newApi = self.repository.save(newApi)
                    self.printSuccess(f'"{newApi.key}" : "{newApi.class_name}" added successfully')
                return
            except Exception as exception :
                errorMessage = str(exception)
        else :
            errorMessage = 'failed to parse parameters'
        globals.error(self.__class__.__class__, f'failed to add api due {commandList} command list', errorMessage)

    def createCredentials(self,commandList):
        self.globals.debug(f'{self.__class__.__name__}.commandList = {commandList}')
        apiKey = apiClassName = gitUrl = None
        try :
            apiKey = commandList[self._0_ARGUMENT]
            apiClassName = commandList[self._1_ARGUMENT]
            if len(commandList[self._2_ARGUMENT:]) > 0 :
                gitUrl = commandList[self._2_ARGUMENT]
            else :
                gitUrl = f'''{self.gitCommitter.gitUrl}/{apiClassName}.{self.gitCommitter.gitExtension}'''
            return apiKey, apiClassName, gitUrl
        except Exception as exception :
            print(f'''{self.globals.ERROR}{self.__class__.__name__} error handling commandList "{commandList}". Cause: {str(exception)}''')

    @SessionMethod
    def printCommandList(self,commandList):
        self.globals.printTree(self.commandList,f'{self.__class__.__name__} commandList',depth=1)

    def printSuccess(self,message):
        print(f'{self.globals.TAB}{self.globals.SUCCESS}{message}')

    def printError(self,message):
        print(f'{self.globals.TAB}{self.globals.ERROR}{message}')


def run(*args,**kwargs):
    ###- ...*args, externalFunction, globals, **kwargs
    import sys
    externalFunction = args[-2]
    globals = args[-1]
    commandList = sys.argv.copy()[1:]
    if len(commandList) > 0 :
        framework = PythonFramework(*args,**kwargs)
        sys.argv = []
        framework.handleSystemArgumentValue(commandList,externalFunction)
    else :
        globals.debug(f'''Command list not found. Proceeding by default api launch''')
        externalFunction(commandList,globals,**kwargs)
