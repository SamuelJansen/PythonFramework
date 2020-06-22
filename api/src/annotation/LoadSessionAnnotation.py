import Constant
import Session, FrameworkConstant

FrameworkStatus = FrameworkConstant.Status
Session = Session.Session


def LoadSession(function,*args,**kwargs) :
    def innerFunction(*args,**kwargs) :
        try :
            self = args[0]
            self.session = self.repository.findByStatus(FrameworkStatus[FrameworkConstant.ACTIVE], Session)
            if self.session :
                self.globals.success(self.__class__, f'"{self.session.key}" session loaded successfully')
            else :
                self.globals.failure(self.__class__,'session not found',self.globals.NOTHING)
            self.loadApiClassSet()
        except Exception as exception :
            print(f'''{Constant.WRAPPER}Failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return innerFunction
