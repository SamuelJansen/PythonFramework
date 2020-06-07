import StringHelper
import Constant as c

def equal(responseAsDict,expectedResponseAsDict) :
    filteredResponse = StringHelper.filterJson(str(responseAsDict))
    filteredExpectedResponse = StringHelper.filterJson(str(expectedResponseAsDict))
    return filteredResponse == filteredExpectedResponse

def filterIgnoreKeyList(objectAsDictionary,ignoreKeyList):
    if objectAsDictionary and ignoreKeyList :
        filteredObjectAsDict = {}
        for key in sorted(objectAsDictionary):
            if key not in ignoreKeyList :
                if objectAsDictionary[key].__class__.__name__ == 'dict' :
                    objectAsDictionary[key] = filterIgnoreKeyList(objectAsDictionary[key],ignoreKeyList)
                filteredObjectAsDict[key] = objectAsDictionary[key]
        return filteredObjectAsDict
    return objectAsDictionary
