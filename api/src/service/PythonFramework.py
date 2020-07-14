import webbrowser
from FrameworkModel import Model
import SqlAlchemyHelper, GitCommitter
import Api, Session
import FrameworkConstant
from LoadSessionAnnotation import LoadSession
from SessionMethodAnnotation import SessionMethod
from PythonFrameworkApplicationScript import *
import FrameworkNewSession, FrameworkOpenSession, FrameworkPrintSession, FrameworkLoadApiClassSet, FrameworkCloseSession, FrameworkAddToSession
import FrameworkSessionHelper
from python_helper import log, Constant

Api = Api.Api
Session = Session.Session
GitCommitter = GitCommitter.GitCommitter
SqlAlchemyHelper = SqlAlchemyHelper.SqlAlchemyHelper
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
    _4_ARGUMENT = 6

    COMMAND_NEW_SESSION = 'new-session'
    COMMAND_OPEN_SESSION = 'open-session'
    COMMAND_ADD_TO_SESSION = 'add-to-session'
    COMMAND_REMOVE_FROM_SESSION = 'remove-from-session'
    COMMAND_SAVE_SESSION = 'save-session'
    COMMAND_PRINT_SESSION = 'print-session'
    COMMAND_SESSION_COMMAND_LIST = 'session-command-list'
    COMMAND_CLOSE_SESSION = 'close-session'

    COMMAND_LIST_ALL_SESSION = 'list-all-session'

    COMMAND_RUN_FLASK = 'run-flask'

    COMMAND_COMMAND_LIST = 'command-list'

    COMMAND_UPDATE_REQUIREMENTS = 'update-requirements'

    commandList = {
        COMMAND_NEW_SESSION : [],
        COMMAND_OPEN_SESSION : ['sessionKey'],
        COMMAND_ADD_TO_SESSION : ['sessionKey','apiKey','apiProjectName','apiClassName','gitUrl'],
        COMMAND_REMOVE_FROM_SESSION : [],
        COMMAND_SAVE_SESSION : [],
        COMMAND_PRINT_SESSION : [],
        COMMAND_SESSION_COMMAND_LIST : [],
        COMMAND_CLOSE_SESSION : [],
        COMMAND_LIST_ALL_SESSION : [],

        COMMAND_RUN_FLASK : []
    }

    KW_GIT_COMMITTER = API_KEY_GIT_COMMITTER

    @SessionMethod
    def handleCommandList(self,commandList):
        globals = self.globals
        log.debug(self.__class__,f'{self.__class__.__name__}.commandList = {commandList}')
        log.debug(self.__class__,f'session = {self.session}')
        return self.apiSet[commandList[self._0_API_KEY]][commandList[self._1_COMMAND]](commandList)

    @SessionMethod
    def handleSystemArgumentValue(self,commandList,externalFunction):
        globals = self.globals
        try :
            if self.apiClassSet :
                apiClass = self.apiClassSet.get(commandList[self._0_API_KEY])
                if apiClass and apiClass in [self.__class__, GitCommitter] :
                    log.success(self.__class__, f'running {commandList} command list')
                    return self.handleCommandList(commandList)
                elif apiClass :
                    globals.overrideApiTree(apiClass.__name__,package=apiClass.__name__)
                    api = apiClass(*self.args,**self.kwargs)
                    log.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                else :
                    log.failure(self.__class__,f'''couldn't instance api class of {commandList[self._0_API_KEY]}''', Constant.NOTHING)
            else :
                log.debug(self.__class__,f'{commandList[self._0_API_KEY]} key called and running all alone')
                return externalFunction(commandList,globals,**self.kwargs)
        except Exception as exception :
            errorMessage = str(exception)
            if self.MISSING_REQUIRED_ARGUMENT in errorMessage :
                newArgs = *self.args,self.globals
                try :
                    api = apiClass(*newArgs,**self.kwargs)
                    log.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                except Exception as exception :
                    secondErrorMessage = f', after first try: {str(exception)}'
                    newArgs = *self.args,self.session,self.globals
                    try :
                        api = apiClass(*newArgs,**self.kwargs)
                        log.success(self.__class__, f'running {apiClass.__name__}({self.args}, {self.kwargs})')
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
        self.repository = SqlAlchemyHelper(model=Model,globals=self.globals)
        self.importApplicationScriptPath = f'{self.globals.apiPath}{self.globals.baseApiPath}runtime{self.globals.BACK_SLASH}{IMPORT_SCRITP_FILE_NAME}.{self.globals.PYTHON_EXTENSION}'

        self.apiSet = {}
        self.apiSet[self.API_KEY_FRAMEWORK] = {
            self.COMMAND_NEW_SESSION : self.newSession,
            self.COMMAND_ADD_TO_SESSION : self.addToSession,
            self.COMMAND_REMOVE_FROM_SESSION : self.removeFromSession,
            self.COMMAND_SAVE_SESSION : self.saveSession,
            self.COMMAND_OPEN_SESSION : self.openSession,
            self.COMMAND_PRINT_SESSION : self.printSession,
            self.COMMAND_CLOSE_SESSION : self.closeSession,

            self.COMMAND_LIST_ALL_SESSION : self.listAllSession,

            self.COMMAND_SESSION_COMMAND_LIST : self.sessionCommandList,
            self.COMMAND_COMMAND_LIST : self.printCommandList,

            self.COMMAND_RUN_FLASK : self.runFlask,

            self.COMMAND_UPDATE_REQUIREMENTS : self.updateRequirements
        }
        self.apiClassSet = self.loadApiClassSet()
        self.gitCommitter = GitCommitter(self.session,self.globals)
        self.apiSet[self.API_KEY_GIT_COMMITTER] = self.gitCommitter.commandSet

    @LoadSession
    def loadApiClassSet(self):
        return FrameworkLoadApiClassSet.loadApiClassSet(self)

    @SessionMethod
    def updateRequirements(self,commandList):
        self.globals.updateDependencyStatus = True
        self.globals.updateDependencies()
        self.globals.updateDependencyStatus = False

    @SessionMethod
    def runFlask(self,commandList) :
        from PythonFrameworkFlask import app
        webbrowser.open_new('http://127.0.0.1:5000/')
        flaskReturn = app.run()
        return flaskReturn

    @SessionMethod
    def newSession(self,commandList):
        return FrameworkNewSession.newSession(self,commandList)

    @SessionMethod
    def addToSession(self,commandList):
        return FrameworkAddToSession.addToSession(self,commandList)

    @SessionMethod
    def removeFromSession(self,commandList):
        log.debug(self.__class__,f'{self.__class__.__name__}.removeFromSession({commandList})')
        pass

    @SessionMethod
    def saveSession(self,commandList):
        log.debug(self.__class__,f'{self.__class__.__name__}.saveSession({commandList})')
        pass

    @SessionMethod
    def listAllSession(self,commandList):
        self.log.debug(self.__class__,f'{self.__class__.__name__}.listAllSession({commandList})')
        pass

    @SessionMethod
    def openSession(self,commandList):
        return FrameworkOpenSession.openSession(self,commandList)

    @SessionMethod
    def printSession(self,commandList):
        return FrameworkPrintSession.printSession(self,commandList)

    @SessionMethod
    def closeSession(self,commandList):
        return FrameworkCloseSession.closeSession(self,commandList)

    @SessionMethod
    def sessionCommandList(self,commandList):
        self.globals.printTree(self.apiSet,f'{Constant.TAB}Command list: ',depth=2)

    @SessionMethod
    def printCommandList(self,commandList):
        self.globals.printTree(self.commandList,f'{self.__class__.__name__} commandList',depth=1)

    def printSuccess(self,message):
        self.printMessage(message,Constant.SUCCESS)

    def printError(self,message):
        self.printMessage(message,Constant.ERROR)

    def printWarning(self,message):
        self.printMessage(message,Constant.WARNING)

    def printMessage(self,message,level):
        print(f'{Constant.TAB}{level}{message}')


def run(*args,**kwargs):
    '''...*args, externalFunction, globals, **kwargs'''
    import sys
    externalFunction = args[-2]
    globals = args[-1]
    commandList = sys.argv.copy()[1:]
    if len(commandList) > 0 :
        framework = PythonFramework(*args,**kwargs)
        sys.argv = []
        return framework.handleSystemArgumentValue(commandList,externalFunction)
    else :
        log.debug(PythonFramework,f'''Command list not found. Proceeding by default api launch method''')
        return externalFunction(commandList,globals,**kwargs)
