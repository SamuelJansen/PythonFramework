from globals import Globals
globals = Globals(__file__,
    successStatus = True,
    settingStatus = True,
    debugStatus = True,
    warningStatus = True,
    failureStatus = True,
    errorStatus = True
)
print('also here')
import PythonFrameworkFlask
app = PythonFrameworkFlask.app
api = PythonFrameworkFlask.api
print('after also here')

if __name__ == '__main__' :
    app.run(debug=True)
