import Session, FrameworkConstant

FrameworkStatus = FrameworkConstant.Status
Session = Session.Session

WRAPPER = '[WRAPPER] '

def LoadSession(function,*args,**kwargs) :
    def innerFunction(*args,**kwargs) :
        try :
            PytonFramework = args[0]
            PytonFramework.session = PytonFramework.repository.findByStatus(FrameworkStatus[FrameworkConstant.ACTIVE], Session)
            if PytonFramework.session :
                PytonFramework.globals.success(PytonFramework.__class__, f'"{PytonFramework.session.key}" session loaded successfully')
            else :
                PytonFramework.globals.failure(PytonFramework.__class__,'session not found',PytonFramework.globals.NOTHING)
            PytonFramework.loadApiClassSet()
        except Exception as exception :
            print(f'''{WRAPPER}Failed to load framework session. Cause: {str(exception)}''')
        return function(*args,**kwargs)
    return innerFunction

def SessionMethod(function,*args,**kwargs) :
    def innerFunction(*args,**kwargs) :
        try :
            PytonFramework = args[0]
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
