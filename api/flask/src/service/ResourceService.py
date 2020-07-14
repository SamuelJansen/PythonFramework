import globals, SqlAlchemyHelper
import FrameworkModel
import HomeController, ConfigController, SessionController, ApiController

print(f'__file__ {__file__}')
controllerList = [
    HomeController.HomeController,
    ConfigController.ConfigController,
    SessionController.SessionController,
    ApiController.ApiController
]

def addControllerTo(api) :
    for controller in controllerList :
        api.add_resource(controller, controller.url)

def addRepositoryTo(api) :
    api.repository = SqlAlchemyHelper.SqlAlchemyHelper(
        model = FrameworkModel.Model,
        globals = api.globals
    )

def addApiResourcesTo(api) :
    globals.addTo(api)
    addRepositoryTo(api)
    addControllerTo(api)

print(f'after __file__ {__file__}')
