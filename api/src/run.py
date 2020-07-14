from globals import Globals
print("run")
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True
)
print("after run")

def pythonFrameworkDefaultRun(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRun()" method not implemented')

if __name__ == '__main__' :
    globals.giveLocalVisibilityToFrameworkApis([
        'globals',
        'python_helper',
        'python_selenium_helper',
        'swagger_integration_tests'
    ])
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRun,globals)
