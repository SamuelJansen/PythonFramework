print('[ResourceService] globals importing')
import globals
print('[ResourceService] globals imported')

print('[ResourceService] SqlAlchemy importing')
import SqlAlchemyHelper
print('[ResourceService] SqlAlchemy imported')

print('[ResourceService] FrameworkModel importing')
import FrameworkModel
print('[ResourceService] FrameworkModel imported')

print('[ResourceService] controllers importing')
import HomeController, ConfigController, SessionController, ApiController
print('[ResourceService] controllers imported')

controllerList = [
    HomeController.HomeController,
    ConfigController.ConfigController,
    SessionController.SessionController,
    ApiController.ApiController
]

def addControllerTo(api) :
    print('[ResourceService] addControllerTo()')
    for controller in controllerList :
        api.add_resource(controller, controller.url)
    print('[ResourceService] addControllerTo() done')

def addRepositoryTo(api) :
    print('[ResourceService] addRepositoryTo()')
    api.repository = SqlAlchemyHelper.SqlAlchemyHelper(
        model = FrameworkModel.Model,
        globals = api.globals
    )
    print('[ResourceService] addRepositoryTo() done')

def addApiResourcesTo(api) :
    print('[ResourceService] addApiResourcesTo()')
    globals.addTo(api)
    addRepositoryTo(api)
    addControllerTo(api)
    print('[ResourceService] addApiResourcesTo() done')
