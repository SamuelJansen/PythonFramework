import SwaggerIntegrationTests, ObjectHelper

integration = SwaggerIntegrationTests

def runTestSet(swagger,testSet) :
    for tagSet in testSet.keys() :
        for testName in testSet[tagSet] :
            testCase = swagger.getTestCase(tagSet,testName)
            for testCaseKey,testCaseValues in testCase.items() :
                runTestCase(swagger,tagSet,testCaseKey,testCaseValues)

def runTestCase(swagger,tagSet,testCaseKey,testCaseValues) :
    url = getUrl(swagger,testCaseValues)
    tag = getTag(swagger,testCaseValues,tagSet)
    method = swagger.getFilteredSetting(integration.METHOD,testCaseValues)
    verb = swagger.getFilteredSetting(integration.VERB,testCaseValues)
    processingTime = swagger.getFilteredSetting(integration.PROCESSING_TIME,testCaseValues)
    payload = swagger.getFilteredSetting(integration.PAYLOAD,testCaseValues)
    expectedResponse = swagger.getFilteredSetting(integration.EXPECTED_RESPONSE,testCaseValues)
    ignoreKeyList = getIgnoreKeyList(swagger,testCaseValues)

    # print(f'ignoreKeyList = {ignoreKeyList}')

    response = swagger.runTest(url,tag,method,verb,processingTime,payload,expectedResponse)

    filteredExpectedResponse = ObjectHelper.filterIgnoreKeyList(expectedResponse,ignoreKeyList,globals)
    filteredResponse = ObjectHelper.filterIgnoreKeyList(response,ignoreKeyList,globals)

    # print(f'filteredExpectedResponse = {filteredExpectedResponse}')
    # print(f'filteredResponse = {filteredResponse}')

    success = ObjectHelper.equal(filteredResponse,filteredExpectedResponse)
    print(f'''
        {testCaseKey}''',end='')
    if success :
        print(f'''
            {integration.SUCCESS_MESSAGE}''')
    else :
        print(f'''
            {integration.URL} = {url}
            {integration.TAG} = {tag}
            {integration.METHOD} = {method}
            {integration.VERB} = {verb}
            {integration.PROCESSING_TIME} = {processingTime}
            {integration.PAYLOAD} = {payload}
            {integration.EXPECTED_RESPONSE} = {expectedResponse}
            {integration.RESPONSE} = {response}''')

def getUrl(swagger,testCaseValues) :
    url = swagger.getFilteredSetting(integration.URL,testCaseValues)
    if not url :
        return swagger.mainUrl
    return url

def getTag(swagger,testCaseValues,tagSet) :
    tag = swagger.getFilteredSetting(integration.TAG,testCaseValues)
    if not tag :
        return tagSet
    return tag

def getIgnoreKeyList(swagger,testCaseValues) :
    ignoreKeyList = swagger.getFilteredSetting(integration.IGNORE_KEY_VALUE_LIST,testCaseValues)
    if ignoreKeyList :
        return ignoreKeyList
    return []
