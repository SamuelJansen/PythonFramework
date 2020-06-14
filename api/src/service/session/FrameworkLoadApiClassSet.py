import Api, Session
Api = Api.Api
Session = Session.Session

import FrameworkConstant
FrameworkStatus = FrameworkConstant.Status

def loadApiClassSet(self) :
    self.globals.debug(f'Loading api class set of {self.__class__.__name__}')
    if self.session :
        for api in self.session.api_list :
            if api.key not in self.apiClassSet.keys() :
                self.apiClassSet[api.key] = loadApiClass(self,api)
    # self.globals.printTree(self.apiClassSet,f'{self.globals.TAB}Class set: ',depth=2)

def loadApiClass(self,api) :
    if api.class_name not in self.globals.apiNameList :
        self.globals.makeApiAvaliable(api.class_name)
        self.globals.printTree(self.globals.apiTree,'globals.apiTree')
    try :
        with open(self.importApplicationScriptPath,self.globals.OVERRIDE,encoding = self.globals.ENCODING) as scriptFile :
            scriptFile.write(''.join(api.import_script))
        from ImportApplicationScript import getApiClass
        apiClass = getApiClass()
        eraseImportApplicationScript(self)
        return apiClass
    except Exception as exception :
        print(f'{self.globals.ERROR}Not possible to reach {api.key} due command line. Cause: {str(exception)}')

def eraseImportApplicationScript(self) :
    blankScript = ''
    with open(self.importApplicationScriptPath,self.globals.OVERRIDE,encoding = self.globals.ENCODING) as scriptFile :
        scriptFile.write(''.join(blankScript))
