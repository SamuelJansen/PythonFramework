import SeleniumHelper, SqlAlchemyHelper

FILE_FOLDER_LOCAL_PATH = 'repository\\file\\'

KW_API = 'api'
KW_NAME = 'name'
KW_MAIN_URL = 'main-url'

DATABASE_LAST_NAME = 'database'

class WebScrapHelper(SeleniumHelper.SeleniumHelper):

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
            print(f'Missing api key:"{globals.CIFRAS_CLUB_WEB_SCRAPER}"')

    def __init__(self,globals,**kwargs):
        SeleniumHelper.SeleniumHelper.__init__(self,globals,**kwargs)
        self.name = self.globals.getApiSetting(f'{KW_API}.{KW_NAME}')
        self.mainUrl = self.globals.getApiSetting(f'{KW_API}.{KW_MAIN_URL}')
        self.repositoryName = f'{self.name}-{DATABASE_LAST_NAME}'
        self.repository = SqlAlchemyHelper.SqlAlchemyHelper(self.repositoryName)
        self.repository.run()

    def run(self,commandList):
        self.globals.debug(f'[{self.globals.apiName}] run() method not implemented')

    def accessMainUrl(self):
        return self.accessUrl(self.mainUrl)
