import globals, SqlAlchemyHelper
from FrameworkModel import Model
import HomeController, GlobalsController, SessionController

controllerList = [
    HomeController.HomeController,
    GlobalsController.GlobalsController,
    SessionController.SessionController
]

def addControllerTo(api) :
    for controller in controllerList :
        api.add_resource(controller, controller.url)

def addRepositoryTo(api) :
    api.repository = SqlAlchemyHelper.SqlAlchemyHelper(model=Model,globals=api.globals)

def addApiResourcesTo(api) :
    globals.addTo(api)
    addControllerTo(api)
