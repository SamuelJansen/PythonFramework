def pythonFrameworkDefaultRun(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRun()" method not implemented')

if __name__ == '__main__' :
    from service.framework.globals import Globals
    globals = Globals.Globals(
        debugStatus = False,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = False
    )
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRun,globals)
