import globals
globalsInstance = globals.newGlobalsInstance(__file__,
    loadLocalConfig = True,
    settingStatus = True,
    successStatus = True,
    errorStatus = True,
    debugStatus = True,
    warningStatus = True,
    infoStatus = True,
    # wrapperStatus = True,
    failureStatus = True
    # logStatus = True
    # testStatus = True,
)

def pythonFrameworkDefaultRunMethod(commandList,globals,**kwargs):
    globalsInstance.debug(f'"pythonFrameworkDefaultRunMethod()" method not implemented')

if __name__ == '__main__' :
    # globalsInstance.giveLocalVisibilityToFrameworkApis([
    #     'globals',
    #     'python_helper'
    #     , 'python_selenium_helper',
    #     'swagger_integration_tests'
    # ])
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRunMethod,globalsInstance)
