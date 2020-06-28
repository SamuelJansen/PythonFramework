import Constant

def SessionMethod(function,*args,**kwargs) :
    def wraperMethod(*args,**kwargs) :
        try :
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
            print(f'''{Constant.WRAPPER}{SessionMethod.__name__} failed to execute{className}{methodName} method. Cause: {str(exception)}''')
    return wraperMethod
