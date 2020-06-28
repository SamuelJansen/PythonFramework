import GitCommitter
GitCommitter = GitCommitter.GitCommitter

import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def loadApiClassSet(self) :
    apiClassSet = {
        self.API_KEY_FRAMEWORK : self.__class__,
        self.API_KEY_GIT_COMMITTER : GitCommitter
    }
    self.globals.debug(f'Loading api class set of {self.__class__.__name__}')
    if self.session :
        for api in self.session.api_list :
            if api.key not in apiClassSet.keys() :
                apiClassSet[api.key] = loadApiClass(self,api)
    if self.globals.debugStatus :
        self.globals.printTree(self.globals.apiTree,f'{self.__class__.__name__} apiTree',depth=1)
        self.globals.printTree(apiClassSet,f'{self.__class__.__name__} api class set',depth=1)
    return apiClassSet

def loadApiClass(self,api) :
    print()
    print(api.key, api.class_name)
    if api.class_name not in self.globals.apiNameList :
        self.globals.makeApiAvaliable(api.class_name)
    try :
        with open(self.importApplicationScriptPath,self.globals.OVERRIDE,encoding = self.globals.ENCODING) as scriptFile :
            scriptFile.write(''.join(api.import_script))
        import Import
        apiClass = Import.getApiClass()
        eraseImportApplicationScript(self)
        return apiClass
    except Exception as exception :
        self.globals.error(self.__class__,f'Not possible to reach {api.key} due command line',exception)

def eraseImportApplicationScript(self) :
    blankScript = ''
    with open(self.importApplicationScriptPath,self.globals.OVERRIDE,encoding = self.globals.ENCODING) as scriptFile :
        scriptFile.write(''.join(blankScript))
