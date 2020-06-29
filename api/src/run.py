import sys

def pythonFrameworkDefaultRun(commandList,globals,**kwargs):
    globals.debug(f'"pythonFrameworkDefaultRun()" method not implemented')

if __name__ == '__main__' :
    from service.framework.globals import Globals
    globals = Globals.Globals(
        debugStatus = True,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = True
    )
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRun,globals)

elif not __name__ == 'run' :
    from api.src.service.framework.globals import Globals
    globals = Globals.Globals(
        debugStatus = True,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = True
    )
    import PythonFrameworkFlask
    ###- It's a Flask build
    app = PythonFrameworkFlask.application
    app.run(debug=True)
    
else :
    import Globals
    globals = Globals.Globals(
        debugStatus = True,
        errorStatus = True,
        successStatus = True,
        failureStatus = True,
        settingStatus = True
    )
    import PythonFrameworkFlask
    app = PythonFrameworkFlask.application
