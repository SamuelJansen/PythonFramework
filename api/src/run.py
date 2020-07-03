def pythonFrameworkDefaultRun(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRun()" method not implemented')

from service.framework.globals import Globals
globals = Globals.Globals(
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
