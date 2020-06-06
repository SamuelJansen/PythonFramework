def pythonFrameworkDefaultRunMethod(commandList,globals,**kwargs):
    globals.debug(f'pythonFrameworkDefaultRunMethod not implemented')

if __name__ == '__main__' :
    from service.framework.globals import Globals
    globals = Globals.Globals(debugStatus = True)
    import PythonFramework
    PythonFramework.run(pythonFrameworkDefaultRunMethod,globals)
