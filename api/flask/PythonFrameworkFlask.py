import flask
import flask_restful
import ResourceService

app = flask.Flask(__name__)
api = flask_restful.Api(app)

ResourceService.addApiResourcesTo(api)
