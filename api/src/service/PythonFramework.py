import SqlAlchemyHelper, GitCommitter
import Api, Session

Api = Api.Api
Session = Session.Session
GitCommitter = GitCommitter.GitCommitter
SqlAlchemyHelper = SqlAlchemyHelper.SqlAlchemyHelper

IMPORT_SCRITP_FILE_NAME = 'ImportApplicationScript'
APPLICATION_TOKEN = '__APPLICATION_TOKEN__'
ADD_APPLICATION_FILE_SCRIPT = f'''
import {APPLICATION_TOKEN}
def getApiClass():
    return {APPLICATION_TOKEN}.{APPLICATION_TOKEN}
'''

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

    KW_ADD_API = 'add-api-by-key-value-pair'
    KW_GIT_COMMITTER = API_KEY_GIT_COMMITTER

    def handleCommandList(self,commandList):
        globals = self.globals
        print(f'PythonFramework.commandList = {commandList}')
        globals.printTree(self.apiSet,'apiSet')
        return self.apiSet[commandList[self._0_API_KEY]][commandList[self._1_COMMAND]](commandList)

    def handleSystemArgumentValue(self,commandList,externalFunction):
        globals = self.globals
        # globals.debug(f'{PythonFramework.__name__}.apiClassSet = {self.apiClassSet}')
        try :
            if self.apiClassSet :
                apiClass = self.apiClassSet.get(commandList[self._0_API_KEY])
                if apiClass and apiClass in [PythonFramework, GitCommitter] :
                    print(f'{globals.SUCCESS}{self.__class__.__name__} running {commandList} command list')
                    return self.handleCommandList(commandList)
                elif apiClass :
                    globals.overrideApiTree(apiClass.__name__)
                    api = apiClass(*self.args,**self.kwargs)
                    print(f'{globals.SUCCESS}{self.__class__.__name__} running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                else :
                    print(f'''{globals.ERROR}{PythonFramework.__name__} api class not found''')
            else :
                globals.debug(f'{commandList[self._0_API_KEY]} key called and running all alone')
                return externalFunction(commandList,globals,**self.kwargs)
        except Exception as exception :
            errorMessage = str(exception)
            globals.debug(f'''{PythonFramework.__name__} error processing "{commandList[self._0_API_KEY]}" call. Cause: {errorMessage}. Going for second attempt''')
            if self.MISSING_REQUIRED_ARGUMENT in errorMessage :
                newArgs = *self.args,globals
                try :
                    api = apiClass(*newArgs,**self.kwargs)
                    print(f'{globals.SUCCESS}{self.__class__.__name__} running {apiClass.__name__}({self.args}, {self.kwargs})')
                    return api.handleCommandList(commandList)
                except Exception as exception :
                    secondErrorMessage = f' after first try: {str(exception)}'
            else :
                secondErrorMessage = ''
            print(f'''{globals.ERROR}{PythonFramework.__name__} error processing "{commandList[self._0_API_KEY]}" call{secondErrorMessage}. Cause: {errorMessage}''')

    def __init__(self,*args,**kwargs):
        self.globals = args[-1]
        externalFunction = args[-2]
        self.args = args[:-2]
        self.kwargs = kwargs
        self.name = self.globals.getApiSetting('api.name')
        self.repositoryName = self.name
        self.repository = SqlAlchemyHelper(self.repositoryName)
        self.repository.run()
        self.session = None
        self.gitCommitter = GitCommitter(self.globals)
        self.importApplicationScriptPath = f'{self.globals.apiPath}{self.globals.baseApiPath}runtime{self.globals.BACK_SLASH}{IMPORT_SCRITP_FILE_NAME}.{self.globals.PYTHON_EXTENSION}'

        self.apiSet = {}
        self.apiSet[self.API_KEY_FRAMEWORK] = {
            self.KW_ADD_API : self.addApi
        }
        self.apiSet[self.API_KEY_GIT_COMMITTER] = self.gitCommitter.commandSet

        self.apiClassSet = self.getApiClassSet()

    def addToSession(self,commandList):
        pass

    def removeFromSession(self,commansList):
        pass

    def saveSession(self,commandList):
        pass

    def openSession(self,commandList):
        pass

    def loadSession(self,commandList):
        pass

    def getApiClassSet(self):
        apiClassSet = {
            self.API_KEY_FRAMEWORK : PythonFramework,
            self.API_KEY_GIT_COMMITTER : GitCommitter
        }
        apiList = self.repository.findAll(Api)
        for api in apiList :
            if api.key not in apiClassSet.keys() :
                apiClassSet[api.key] = self.loadApiClass(api)
        return apiClassSet

    def addApi(self,commandList):
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
                        newSession = Session(sessionKey,[])
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
                        print(f'{globals.SUCCESS}"{api.key}" : "{api.class_name}" added successfully')
                    globals.debug(f'{globals.TAB}{globals.WARNING}"{api.key}" : "{api.class_name}" already belongs to "{self.session.key}" session')
                else :
                    newApi = Api(apiKey,apiClassName,gitUrl,importApplicationScript,[self.session])
                    print(f'newApi = {newApi}')
                    newApi = self.repository.save(newApi)
                    print(f'{globals.SUCCESS}"{newApi.key}" : "{newApi.class_name}" added successfully')
                return
            except Exception as exception :
                errorMessage = str(exception)
        else :
            errorMessage = 'failed to parse parameters'
        print(f'''{globals.ERROR}{PythonFramework.__name__} failed to add api due {commandList} command list. Cause: {errorMessage}''')

    def loadApiClass(self,api):
        globals = self.globals
        if api.class_name not in globals.apiNameList :
            globals.makeApiAvaliable(api.class_name)
            globals.printTree(globals.apiTree,'globals.apiTree')
        try :
            with open(self.importApplicationScriptPath,globals.OVERRIDE,encoding = globals.ENCODING) as scriptFile :
                scriptFile.write(''.join(api.import_script))
            from ImportApplicationScript import getApiClass
            apiClass = getApiClass()
            self.eraseImportApplicationScript()
            return apiClass
        except Exception as exception :
            print(f'{globals.ERROR}Not possible to reach {api.key} due command line. Cause: {str(exception)}')

    def eraseImportApplicationScript(self):
        blankScript = ''
        with open(self.importApplicationScriptPath,self.globals.OVERRIDE,encoding = self.globals.ENCODING) as scriptFile :
            scriptFile.write(''.join(blankScript))

    def createCredentials(self,commandList):
        print(f'commandList = {commandList}')
        apiKey = apiClassName = gitUrl = None
        try :
            _0_API_KEY = 0
            _1_COMMAND = 1
            _0_ARGUMENT = 2
            _1_ARGUMENT = 3
            _2_ARGUMENT = 4
            apiKey = commandList[self._0_ARGUMENT]
            apiClassName = commandList[self._1_ARGUMENT]
            if len(commandList[self._2_ARGUMENT:]) > 0 :
                gitUrl = commandList[self._2_ARGUMENT]
            else :
                gitUrl = f'''{self.gitCommitter.gitUrl}/{apiClassName}.{self.gitCommitter.gitExtension}'''
            return apiKey, apiClassName, gitUrl
        except Exception as exception :
            print(f'''{self.globals.ERROR}{PythonFramework.__name__} invalid commandList "{commandList}". Cause: {str(exception)}''')

    def getCredentials(self,commandList):
        apiKey = apiClassName = None
        try :
            Api = self.repository.findByKey(apiKey,Api)
            apiClassName = commandList[1]
            return apiKey, apiClassName
        except Exception as exception :
            print(f'''{self.globals.ERROR}{PythonFramework.__name__} invalid commandList "{commandList}". Cause: {str(exception)}''')

    def updateApiSet(self,apiKey,apiClass):
        self.apiClassSet[apiKey] = apiClass

    def apiNotFound(self,apiKey,cause):
        self.globals.debug


def run(*args,**kwargs):
    ###- ..., externalFunction, globals, **kwargs
    import sys
    externalFunction = args[-2]
    globals = args[-1]
    commandList = sys.argv.copy()[1:]
    if len(commandList) > 0 :
        framework = PythonFramework(*args,**kwargs)
        framework.handleSystemArgumentValue(commandList,externalFunction)
    else :
        globals.debug(f'''Command list not found. Proceeding by default api launch''')
        externalFunction(commandList,globals,**kwargs)
