def pythonFrameworkDefaultRun(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRun()" method not implemented')

try :
    from globals import Globals
    globals = Globals(
        filePath = __file__,
        debugStatus = True,
        warningStatus = True,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = True
    )
except Exception as exception :
    print(exception)
    from service.framework.globals import Globals
    Globals = Globals.Globals
    globals = Globals(
        file = __file__,
        debugStatus = True,
        warningStatus = True,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = True
    )

if __name__ == '__main__' :
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRun,globals)
