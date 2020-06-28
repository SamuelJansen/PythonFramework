import importlib
def getApiClass() :
    from runtime import ImportApplicationScript
    importlib.reload(ImportApplicationScript)
    return ImportApplicationScript.getApiClass()
