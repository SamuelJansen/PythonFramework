from python_helper import Constant
from python_helper import log

def SessionMethod(sessionMethod,*args,**kwargs) :
    def wraperMethod(*args,**kwargs) :
        try :
            return sessionMethod(*args,**kwargs)
        except Exception as exception :
            try :
                className = f' {args[0].__class__.__name__}'
            except :
                className = ''
            try :
                methodName = sessionMethod.__name__
                if not className == '' :
                    methodName = f'.{methodName}'
                else :
                    methodName = f' {methodName}'
            except :
                methodName = ''
            log.wraper(SessionMethod,f'''failed to execute{className}{methodName} method''',exception)
    return wraperMethod
