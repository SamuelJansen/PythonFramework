import Constant
import Api, Session, FrameworkConstant
from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, APPLICATION_TOKEN

FrameworkStatus = FrameworkConstant.Status
Session = Session.Session
Api = Api.Api


def LoadSession(function,*annotatinArgs,**annotationKwargs) :
    def wraperMethod(*args,**kwargs) :
        try :
            self = args[0]
            self.session = self.repository.findByStatus(FrameworkStatus[FrameworkConstant.ACTIVE], Session)
            if self.session :
                self.globals.success(self.__class__, f'"{self.session.key}" session loaded successfully')
            else :
                self.session = getBasicSession(self)
                self.globals.failure(self.__class__,f'''couldn't find any active session. Running "{self.session.key}" session.''',self.globals.NOTHING)
        except Exception as exception :
            print(f'''{Constant.WRAPPER}{SessionMethod.__name__} failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return wraperMethod

def getBasicSession(self) :
    basicSessionKey = self.globals.getApiSetting('api.basic.session.key')
    apiList = getDefaultApiList(self)
    return Session(basicSessionKey, FrameworkConstant.ACTIVE, apiList)

def getDefaultApiList(self) :
    gitUrl = self.globals.getApiSetting('api.git.url')
    gitExtension = self.globals.getApiSetting('api.git.extension')
    apiKey = self.globals.getApiSetting('api.basic.api.key')
    apiClassName = self.globals.getApiSetting('api.basic.api.class-name')
    importScript = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
    sessionList = []
    return [Api(apiKey,apiClassName,f'''{gitUrl}/{apiClassName}.{gitExtension}''',import_script, sessionList)]
