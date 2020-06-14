import Session, FrameworkConstant

FrameworkStatus = FrameworkConstant.Status
Session = Session.Session

WRAPPER = '[WRAPPER] '

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
            print(f'''{WRAPPER}Failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return innerFunction

def SessionMethod(function,*args,**kwargs) :
    def innerFunction(*args,**kwargs) :
        try :
            self = args[0]
            return function(*args,**kwargs)
        except Exception as exception :
            try :
                className = f' {args[0].__class__.__name__}'
            except :
                className = ''
            try :
                methodName = function.__name__
                if not className == '' :
                    methodName = f'.{methodName}'
                else :
                    methodName = f' {methodName}'
            except :
                methodName = ''
            print(f'''{WRAPPER}Failed to execute{className}{methodName} method. Cause: {str(exception)}''')
    return innerFunction
