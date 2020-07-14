from globals import Globals
globals = Globals(__file__,
    successStatus = True,
    settingStatus = True,
    debugStatus = True,
    warningStatus = True,
    failureStatus = True,
    errorStatus = True
)
print(f'__file__ {__file__}')
import PythonFrameworkFlask
app = PythonFrameworkFlask.app
api = PythonFrameworkFlask.api
print(f'after __file__ {__file__}')

if __name__ == '__main__' :
    app.run(debug=True)
