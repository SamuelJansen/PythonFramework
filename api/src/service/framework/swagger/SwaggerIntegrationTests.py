import SeleniumHelper, SwaggerTestRunner, SettingHelper

INTEGRATION_FOLDER = 'integration'

KW_MAIN_SWAGGER_URL = 'main-swagger-url'
KW_TEST_CASE = 'testCase'
KW_INTEGRATION = INTEGRATION_FOLDER

URL = 'url'
TAG = 'tag'
METHOD = 'method'
VERB = 'verb'
PROCESSING_TIME = 'processingTime'
PAYLOAD = 'payload'
EXPECTED_RESPONSE = 'expectedResponse'
RESPONSE = 'response'
IGNORE_KEY_VALUE_LIST = 'ignore-key-value-list'

SUCCESS_MESSAGE = 'Success'

class SwaggerIntegrationTests(SeleniumHelper.SeleniumHelper):

    def __init__(self,globals,**kwargs):
        SeleniumHelper.SeleniumHelper.__init__(self,globals,**kwargs)
        self.integrationPath = f'{globals.apiPath}{globals.baseApiPath}{INTEGRATION_FOLDER}{globals.BACK_SLASH}'
        self.mainSwaggerUrlFilePath = f'{self.integrationPath}{KW_INTEGRATION}.{self.globals.extension}'
        self.mainUrl = self.getFilteredSetting(KW_MAIN_SWAGGER_URL,globals.getSettingTree(settingFilePath=self.mainSwaggerUrlFilePath))

    def runTestSet(self,testSet):
        SwaggerTestRunner.runTestSet(self,testSet)

    def runTest(self,url,tag,method,verb,processingTime,payload,expectedResponse) :
        self.resetValues(url,tag,method,verb,processingTime,payload,expectedResponse)
        swaggerUrl = self.accessSwaggerUrl()
        swaggerTag = self.accessSwaggerTag(swaggerUrl)
        swaggerMethod = self.accessSwaggerMethod(swaggerTag)
        self.hitTryOut(swaggerMethod)
        self.typePayload(swaggerMethod)
        self.hitExecute(swaggerMethod)
        self.waitProcessingTime()
        response = self.getResponse(swaggerMethod)
        return response

    def resetValues(self,url,tag,method,verb,processingTime,payload,expectedResponse):
        globals = self.globals
        self.url = url
        self.tag = tag
        self.method = method
        self.verb = verb
        self.processingTime = processingTime
        self.payload = payload
        self.expectedResponse = expectedResponse
        self.findByIdRequest = f'{SwaggerKeyWord.OPERATION_TAG_DASH}{self.tag.replace(globals.SPACE,globals.UNDERSCORE)}'
        self.accessIdRequest = f'{SwaggerKeyWord.OPERATIONS_DASH}{self.tag}-{self.method}{SwaggerKeyWord.USING}{self.verb}'

    def accessSwaggerUrl(self):
        return self.accessUrl(self.url)

    def accessSwaggerTag(self,swaggerUrl):
        return self.accessClass(SwaggerKeyWord.EXPAND_OPERATION,self.findById(self.findByIdRequest,swaggerUrl))

    def accessSwaggerMethod(self,swaggerTag):
        return self.accessId(self.accessIdRequest,swaggerTag)

    def hitTryOut(self,swaggerMethod):
        self.accessButton(self.findByClass(SwaggerKeyWord.TRY_OUT,swaggerMethod))

    def typePayload(self,swaggerMethod):
        self.typeInSwagger(self.payload,self.findByClass(SwaggerKeyWord.BODY_PARAM,swaggerMethod))

    def hitExecute(self,swaggerMethod):
        self.accessButton(self.findByClass(SwaggerKeyWord.EXECUTE_WRAPPER,swaggerMethod))

    def getResponse(self,swaggerMethod):
        return self.getTextByClass(SwaggerKeyWord.MICROLIGHT,self.findByClass(SwaggerKeyWord.HIGHLIGHT_CODE,swaggerMethod))

    def waitProcessingTime(self):
        self.wait(processingTime=self.processingTime)

    def getFilteredSetting(self,keySetting,testCase):
        return SettingHelper.getFilteredSetting(self.globals.getSetting(keySetting,settingTree=testCase),self.globals)

    def getTestCase(self,tag,testName):
        settingTree = self.globals.getSettingTree(settingFilePath=f'{self.integrationPath}{tag}{self.globals.BACK_SLASH}{testName}.{self.globals.extension}')
        if KW_TEST_CASE in settingTree.keys() :
            newSettingTree = {}
            for settingTreeKey, settingTreeValue in settingTree[KW_TEST_CASE].items() :
                newSettingTree[f'{testName}.{settingTreeKey}'] = settingTreeValue
            return newSettingTree
        return {testName : settingTree}


class SwaggerKeyWord:

    EXPAND_OPERATION = 'expand-operation'
    TRY_OUT = 'try-out'
    BODY_PARAM = 'body-param__text'
    EXECUTE_WRAPPER = 'execute-wrapper'
    HIGHLIGHT_CODE = 'highlight-code'
    MICROLIGHT = 'microlight'

    ###- this seccion is used only as part of the full swagger html class or ir or whatever
    OPERATIONS_DASH = 'operations-'
    OPERATION_TAG_DASH = 'operations-tag-'
    USING = 'Using'
