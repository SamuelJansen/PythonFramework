import SeleniumHelper, SqlAlchemyHelper

FILE_FOLDER_LOCAL_PATH = 'repository\\file\\'

KW_API = 'api'
KW_NAME = 'name'
KW_MAIN_URL = 'main-url'

KW_REPOSITORY = 'repository'
KW_REPOSITORY_DIALECT = 'dialect'
KW_REPOSITORY_USER = 'user'
KW_REPOSITORY_PASSWORD = 'password'
KW_REPOSITORY_HOST = 'host'
KW_REPOSITORY_PORT = 'port'
KW_REPOSITORY_DATABASE = 'database'

DATABASE_LAST_NAME = 'database'

class WebScrapHelper(SeleniumHelper.SeleniumHelper):

    FILE_FOLDER_LOCAL_PATH = FILE_FOLDER_LOCAL_PATH

    DATASET_FILE_NAME = 'dataset'
    SECOND_DATASET_FILE_NAME = 'second-dataset'
    FAILED_DATASET_FILE_NAME = 'failed-dataset'

    _0_API_KEY = 0
    _1_COMMAND = 1
    _0_ARGUMENT = 2
    _1_ARGUMENT = 3
    _2_ARGUMENT = 4

    def handleCommandList(self,commandList):
        commandList = commandList.copy()
        globals = self.globals
        if commandList :
            apiKey = commandList[self._0_API_KEY]
            if len(commandList) > self._1_COMMAND and commandList[self._1_COMMAND] :
                try :
                    if len(commandList) > self._0_ARGUMENT :
                        response = self.commandSet[commandList[self._1_COMMAND]](commandList[self._0_ARGUMENT:])
                    else :
                        response = self.commandSet[commandList[self._1_COMMAND]]([])
                    globals.debug(f'response = {response}')
                    return response
                except Exception as exception :
                    print(f'{globals.ERROR}Failed to execute command: "{commandList[self._1_COMMAND]}". Cause: {str(exception)}')
                    return
            else :
                print(f'Missing command: {list(self.commandSet.keys())}')
        else :
            print(f'Missing api key in command line')

    def __init__(self,globals,**kwargs):
        modelKey = 'model'
        model = kwargs.get(modelKey)
        del kwargs[modelKey]
        SeleniumHelper.SeleniumHelper.__init__(self,globals,**kwargs)
        self.name = self.globals.getApiSetting(f'{KW_API}.{KW_NAME}')

        self.repositoryDialect = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DIALECT}')
        self.repositoryUser = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_USER}')
        self.repositoryPassword = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PASSWORD}')
        self.repositoryHost = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_HOST}')
        self.repositoryPort = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PORT}')
        self.databaseName = self.globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DATABASE}')

        if not self.databaseName :
            self.databaseName = self.name
        self.repository = SqlAlchemyHelper.SqlAlchemyHelper(
            name = self.databaseName,
            dialect = self.repositoryDialect,
            user = self.repositoryUser,
            password = self.repositoryPassword,
            host = self.repositoryHost,
            port = self.repositoryPort,
            model = model
        )

        self.mainUrl = self.globals.getApiSetting(f'{KW_API}.{KW_MAIN_URL}')
        self.commandSet = {}

    def run(self,commandList):
        self.globals.debug(f'[{self.globals.apiName}] run() method not implemented')

    def accessMainUrl(self):
        return self.accessUrl(self.mainUrl)
