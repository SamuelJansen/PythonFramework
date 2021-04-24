import webbrowser
from python_helper import Constant
import GitCommand

GitCommand = GitCommand.GitCommand

def newReleaseAll(self,commandList) :
    try :
        commandSet = {}
        for projectName in self.projectNameList :
            if projectName :
                versionArgumentIndex = self._1_ARGUMENT_INDEX
                commitMessageArgumentIndex = self._2_ARGUMENT_INDEX
                updateCommandSet(self,projectName,versionArgumentIndex,commitMessageArgumentIndex,commandSet,commandList)
            else :
                self.globals.error('Project name cannot be null', Constant.NOTHING)
                return
        return runNewRelease(self,commandSet)
    except Exception as exception :
        print(exception)

def newReleaseProject(self,commandList) :
    try :
        commandSet = {}
        projectName = self.getArg(self._1_ARGUMENT_INDEX,'Project name',commandList)
        if projectName :
            versionArgumentIndex = self._2_ARGUMENT_INDEX
            commitMessageArgumentIndex = self._3_ARGUMENT_INDEX
            updateCommandSet(self,projectName,versionArgumentIndex,commitMessageArgumentIndex,commandSet,commandList)
        else :
            self.globals.error('Project name cannot be null', Constant.NOTHING)
            return
        return runNewRelease(self,commandSet)
    except Exception as exception :
        print(exception)

def runNewRelease(self,commandSet) :
    try :
        returnSet = self.runCommandSet(commandSet)
        self.debugReturnSet('newReleaseAll',self.getReturnSetValue(returnSet))
        return returnSet
    except Exception as exception :
        print(exception)

def getApi(self,projectName) :
    for api in self.session.apiList :
        if projectName == api.projectName :
            return api
    errorMessage = f'project "{projectName}" not found'
    self.globals.error(errorMessage,Constant.NOTHING)
    raise Exception(errorMessage)

def getUrl(self,api) :
    return api.gitUrl.replace(f'{Constant.DOT}{self.gitExtension}',Constant.NOTHING)

def validateVersion(self,version) :
    if not version or Constant.NOTHING == version :
        raise Exception('''Version cannot be null''')
    if 'v' in version or 'v-' in version or 'V' in version or 'V-' in version :
        raise Exception('''Version cannot contain "v" or "V" of "v-" or "V-" charactere''')

def getDescription(self,api) :
    description = '+'.join(self.getImput(f'{api.projectName} description').split())
    if description :
        return description
    return Constant.NOTHING

def getNewReleaseUrl(self,api,version,releaseMessage=None):
    url = GitCommand.NEW_RELEASE
    url = url.replace(GitCommand.TOKEN_PROJECT_URL,getUrl(self,api))
    url = url.replace(GitCommand.TOKEN_RELEASE_VERSION,version)
    url = url.replace(GitCommand.TOKEN_TARGET,api.mainBranch)
    url = url.replace(GitCommand.TOKEN_TITLE,api.projectName)
    url = url.replace(GitCommand.TOKEN_DESCRIPTION,releaseMessage if releaseMessage else getDescription(self,api))
    return url

def updateCommandSet(self,projectName,versionArgumentIndex,commitMessageArgumentIndex,commandSet,commandList) :
    api = getApi(self,projectName)
    version = self.getArg(versionArgumentIndex,f'{api.projectName} release version',commandList)
    validateVersion(self,version)
    commitMessage = self.getArg(commitMessageArgumentIndex,f'{api.projectName} commit message',commandList)
    commitMessageSplited = commitMessage.split(Constant.COLON)
    releaseMessage = commitMessageSplited[0] if 1 == len(commitMessageSplited) or commitMessageSplited[1] is None else Constant.COLON.join(commitMessageSplited[1:])
    webbrowser.open_new(getNewReleaseUrl(self,api,version,releaseMessage=releaseMessage))
    commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
    commandCheckoutMainBranch = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,api.mainBranch)
    commandMergeOriginDevelop = GitCommand.MERGE_ORIGIN.replace(GitCommand.TOKEN_BRANCH_NAME,GitCommand.KW_DEVELOP_BRANCH)
    commandNewDist = self.COMMAND_NEW_DIST
    commandTwineUpload = self.COMMAND_TWINE_UPLOAD.replace(self.TOKEN_PY_PI_USERNAME,self.PyPIUsername)
    commandTwineUpload = commandTwineUpload.replace(self.TOKEN_PY_PI_PASSWORD,self.PyPIPassword)
    commandSet[projectName] = [
        GitCommand.ADD,
        commandCommit,
        GitCommand.PUSH,
        commandCheckoutMainBranch,
        commandMergeOriginDevelop,
        GitCommand.PUSH,
        commandNewDist,
        commandTwineUpload
    ]
