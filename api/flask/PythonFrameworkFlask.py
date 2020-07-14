print(f'[PythonFrameworkFlask] flask stuff importing')
import flask
import flask_restful
print(f'[PythonFrameworkFlask] flask stuff imported')

print(f'[PythonFrameworkFlask] application modules importing')
import ResourceService
print(f'[PythonFrameworkFlask] application modules imported')

print(f'[PythonFrameworkFlask] flask.Flask(__name__)')
app = flask.Flask(__name__)
print(f'[PythonFrameworkFlask] flask.Flask(__name__) done')

print(f'[PythonFrameworkFlask] flask_restful.Api(app)')
api = flask_restful.Api(app)
print(f'[PythonFrameworkFlask] flask_restful.Api(app) done')

print(f'[PythonFrameworkFlask] ResourceService.addApiResourcesTo(api)')
ResourceService.addApiResourcesTo(api)
print(f'[PythonFrameworkFlask] ResourceService.addApiResourcesTo(api) done')
