from api.src.service.framework.globals import Globals
globals = Globals.Globals(
    debugStatus = True,
    errorStatus = True,
    successStatus = True,
    failureStatus = True,
    settingStatus = True
)

import PythonFrameworkFlask
app = PythonFrameworkFlask.application

if __name__ == '__main__' :
    app.run(debug=True)
