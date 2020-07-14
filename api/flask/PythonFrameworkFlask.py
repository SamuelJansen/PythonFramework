import flask
import flask_restful
import ResourceService

print(f'__file__ {__file__}')
app = flask.Flask(__name__)
api = flask_restful.Api(app)
ResourceService.addApiResourcesTo(api)
print(f'after __file__ {__file__}')
