from globals import Globals

print(f'__file__ {__file__}')
globals = Globals(__file__,
    debugStatus = True,
    warningStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True
)

def pythonFrameworkDefaultRunMethod(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRunMethod()" method not implemented')

print(f'after __file__ {__file__}')

if __name__ == '__main__' :
    globals.giveLocalVisibilityToFrameworkApis([
        'globals',
        'python_helper',
        'python_selenium_helper',
        'swagger_integration_tests'
    ])
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRunMethod,globals)
