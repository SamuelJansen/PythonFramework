import globals as globalsModule
import FrameworkModel
import HomeController, ConfigController, SessionController, ApiController

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
    import SqlAlchemyHelper
    api.repository = SqlAlchemyHelper.SqlAlchemyHelper(
        model = FrameworkModel.Model,
        globals = api.globals
    )

def addApiResourcesTo(api) :
    globalsModule.addTo(api)
    addRepositoryTo(api)
    addControllerTo(api)
