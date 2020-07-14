from globals import Globals

print('[app] globals instanciating')
globals = Globals(__file__,
    successStatus = True,
    settingStatus = True,
    debugStatus = True,
    warningStatus = True,
    failureStatus = True,
    errorStatus = True
)
print('[app] globals instanciated')

print(f'[app] PythonFrameworkFlask importing')
import PythonFrameworkFlask
print(f'[app] PythonFrameworkFlask imported')

print(f'[app] PythonFrameworkFlask.app refferenceing')
app = PythonFrameworkFlask.app
print(f'[app] PythonFrameworkFlask.app refferenced')

print(f'[app] PythonFrameworkFlask.api refferenceing')
api = PythonFrameworkFlask.api
print(f'[app] PythonFrameworkFlask.api refferenced')

if __name__ == '__main__' :
    print(f'[app] run()')
    app.run(debug=True)
