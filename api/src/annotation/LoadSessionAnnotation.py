from python_helper import Constant
import Api, Session, FrameworkConstant, DataLoad
from PythonFrameworkApplicationScript import ADD_APPLICATION_FILE_SCRIPT, APPLICATION_TOKEN

FrameworkStatus = FrameworkConstant.Status
Session = Session.Session
Api = Api.Api


def LoadSession(function,*annotatinArgs,**annotationKwargs) :
    def wraperMethod(*args,**kwargs) :
        try :
            self = args[0]
            self.session = self.repository.findByStatusAndCommit(FrameworkStatus[FrameworkConstant.ACTIVE], Session)
            if self.session :
                self.globals.success(self.__class__, f'"{self.session.key}" session loaded successfully')
            else :
                self.session = DataLoad.getBasicSession(self) ###- getBasicSession(self)
                print(f'self.session = {self.session}')
                self.globals.failure(self.__class__,f'''couldn't find any active session. Running most recent version of "{self.session.key}" session.''',self.globals.NOTHING)
        except Exception as exception :
            print(f'''{Constant.WRAPPER}{LoadSession.__name__} failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return wraperMethod
