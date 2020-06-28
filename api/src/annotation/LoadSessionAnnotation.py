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
            print(f'''{Constant.WRAPPER}Failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return wraperMethod

def getBasicSession(self) :
    gitUrl = self.globals.getApiSetting('api.git.url')
    gitExtension = self.globals.getApiSetting('api.git.extension')
    basicSessionKey = self.globals.getApiSetting('api.basic.session.key')
    apiKey = self.globals.getApiSetting('api.basic.api.key')
    apiClassName = self.globals.getApiSetting('api.basic.api.class-name')
    import_script = ADD_APPLICATION_FILE_SCRIPT.replace(APPLICATION_TOKEN,apiClassName)
    sessionList = []
    apiList = [Api(apiKey,apiClassName,f'''{gitUrl}/{apiClassName}.{gitExtension}''',import_script, sessionList)]
    return Session(basicSessionKey, FrameworkConstant.ACTIVE, apiList)
