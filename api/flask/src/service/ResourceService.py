import globals, SqlAlchemyHelper
import FrameworkModel
import HomeController, ConfigController, SessionController

controllerList = [
    HomeController.HomeController,
    ConfigController.ConfigController,
    SessionController.SessionController
]

def addControllerTo(api) :
    for controller in controllerList :
        api.add_resource(controller, controller.url)

def addRepositoryTo(api) :
    print('here')
    api.repository = SqlAlchemyHelper.SqlAlchemyHelper(
        model = FrameworkModel.Model,
        globals = api.globals
    )
    print('after here')

def addApiResourcesTo(api) :
    globals.addTo(api)
    addRepositoryTo(api)
    addControllerTo(api)
