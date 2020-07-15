import subprocess
from python_helper import Constant
import GitCommitterNewRelease

import WakeUpVoiceAssistant, VoiceAssistant, GitCommand
from python_helper import log

GitCommand = GitCommand.GitCommand

class GitCommitter:

    REQUIRES_GLOBALS = True

    GIT_COMMITTER_INDEX = 0
    COMMAND_INDEX = 1
    _1_ARGUMENT_INDEX = 2
    _2_ARGUMENT_INDEX = 3
    _3_ARGUMENT_INDEX = 4
    _4_ARGUMENT_INDEX = 5
    _5_ARGUMENT_INDEX = 6
    _6_ARGUMENT_INDEX = 7

    MISSING_SPACE = 'Missing '

    WAKE_UP_VOICE_ASSISTANT = 'voice-assistant'

    TOKEN_PY_PI_USERNAME = '__TOKEN_PY_PI_USERNAME__'
    TOKEN_PY_PI_PASSWORD = '__TOKEN_PY_PI_PASSWORD__'

    KW_ALL = 'all'
    KW_IF_DASH_NEEDED = 'if-needed'
    KW_PROJECT = 'project'
    KW_NEW_RELEASE = 'new-release'

    SET_GLOBAL_CREDENTIALS = 'set-global-credentials'

    CLONE_ALL_IF_NEEDED = f'{GitCommand.KW_CLONE}-{KW_ALL}-{KW_IF_DASH_NEEDED}'
    CHECKOUT_B_ALL_IF_NEEDED = f'{GitCommand.KW_CHECKOUT}-b-{KW_ALL}-{KW_IF_DASH_NEEDED}'
    PUSH_SET_UPSTREAM_ORIGIN_ALL_IF_NEEDED = f'{GitCommand.KW_PUSH}-{GitCommand.KW_SET_UPSTREAM}-{GitCommand.KW_ORIGIN}-{KW_ALL}-{KW_IF_DASH_NEEDED}'
    ADD_COMMIT_PUSH_SET_UPSTREAM_ORIGIN_ALL_IF_NEEDED = f'{GitCommand.KW_ADD}-{GitCommand.KW_COMMIT}-{GitCommand.KW_PUSH}-{GitCommand.KW_SET_UPSTREAM}-{GitCommand.KW_ORIGIN}-{KW_ALL}-{KW_IF_DASH_NEEDED}'

    STATUS_ALL = f'{GitCommand.KW_STATUS}-{KW_ALL}'
    BRANCH_ALL = f'{GitCommand.KW_BRANCH}-{KW_ALL}'
    PULL_ALL = f'{GitCommand.KW_PULL}-{KW_ALL}'
    CHECKOUT_ALL = f'{GitCommand.KW_CHECKOUT}-{KW_ALL}'
    ADD_ALL = f'{GitCommand.KW_ADD}-{KW_ALL}'
    COMMIT_ALL = f'{GitCommand.KW_COMMIT}-{KW_ALL}'
    PUSH_ALL = f'{GitCommand.KW_PUSH}-{KW_ALL}'
    ADD_COMMIT_PUSH_ALL = f'{GitCommand.KW_ADD}-{GitCommand.KW_COMMIT}-{GitCommand.KW_PUSH}-{KW_ALL}'
    MERGE_ORIGIN_ALL = f'{GitCommand.KW_MERGE}-{GitCommand.KW_ORIGIN}-{KW_ALL}'

    CLONE_PROJECT_IF_NEEDED = f'{GitCommand.KW_CLONE}-{KW_PROJECT}-{KW_IF_DASH_NEEDED}'
    ADD_COMMIT_PUSH_PROJECT = f'{GitCommand.KW_ADD}-{GitCommand.KW_COMMIT}-{GitCommand.KW_PUSH}-{KW_PROJECT}'

    COMMAND_NEW_DIST = 'python setup.py sdist'
    COMMAND_TWINE_UPLOAD = f'twine upload -u {TOKEN_PY_PI_USERNAME} -p {TOKEN_PY_PI_PASSWORD} dist/*'

    NEW_RELEASE_ALL = f'{KW_NEW_RELEASE}-{KW_ALL}'
    NEW_RELEASE_PROJECT = f'{KW_NEW_RELEASE}-{KW_PROJECT}'

    DEPLOY_HEROKU_PROJECT = 'deploy-heroku-project'

    ADD_ENVIRONMENT_VARIABLE = 'add-environment-variable'

    SKIP = 'skip'

    CONFIRM = ['execute']

    def handleCommandList(self,commandList):
        print(f'GitCommitter.commandList = {commandList}')
        globals = self.globals
        if len(commandList) < GitCommitter.COMMAND_INDEX :
            print(f'{globals.ERROR}{GitCommitter.MISSING_SPACE}{GitCommand.API_KEY_GIT_COMMITTER} command')
            return
        gitCommiterCallCommand = commandList[GitCommitter.GIT_COMMITTER_INDEX]
        command = commandList[GitCommitter.COMMAND_INDEX]
        if GitCommand.API_KEY_GIT_COMMITTER == gitCommiterCallCommand :
            try :
                return self.commandSet[command](commandList)
            except Exception as exception :
                print(f'''{globals.ERROR}Error processing command "{gitCommiterCallCommand} {command}": {str(exception)}''')

    def __init__(self,session,globals):
        self.globals = globals
        self.session = session
        self.projectNameList = self.getProjectNameList()
        self.gitUrl = globals.getApiSetting(f'api.git.url')
        self.gitExtension = globals.getApiSetting(f'api.git.extension')
        self.PyPIUsername = globals.getApiSetting(f'api.git.PyPI.username')
        self.PyPIPassword = globals.getApiSetting(f'api.git.PyPI.password')
        self.commandSet = {
            GitCommitter.WAKE_UP_VOICE_ASSISTANT : self.wakeUpVoiceAssistant,

            GitCommitter.SET_GLOBAL_CREDENTIALS : self.setGlobalCredentials,

            GitCommitter.CLONE_ALL_IF_NEEDED : self.cloneAllIfNeeded,
            GitCommitter.CHECKOUT_B_ALL_IF_NEEDED : self.checkoutBAllIfNeeded,
            GitCommitter.PUSH_SET_UPSTREAM_ORIGIN_ALL_IF_NEEDED : self.pushSetUpStreamOriginAllIfNedded,
            GitCommitter.ADD_COMMIT_PUSH_SET_UPSTREAM_ORIGIN_ALL_IF_NEEDED : self.addCommitPushSetUpStreamOriginAllIfNedded,

            GitCommitter.STATUS_ALL : self.statusAll,
            GitCommitter.BRANCH_ALL : self.branchAll,
            GitCommitter.PULL_ALL : self.pullAll,
            GitCommitter.CHECKOUT_ALL : self.checkoutAll,
            GitCommitter.ADD_ALL : self.addAll,
            GitCommitter.COMMIT_ALL : self.commitAll,
            GitCommitter.PUSH_ALL : self.pushAll,
            GitCommitter.ADD_COMMIT_PUSH_ALL : self.addCommitPushAll,
            GitCommitter.MERGE_ORIGIN_ALL : self.mergeOriginAll,

            GitCommitter.CLONE_PROJECT_IF_NEEDED : self.cloneProjectIfNeeded,
            GitCommitter.ADD_COMMIT_PUSH_PROJECT : self.addCommitPushProject,

            GitCommitter.NEW_RELEASE_ALL : self.newReleaseAll,
            GitCommitter.NEW_RELEASE_PROJECT : self.newReleaseProject,

            GitCommitter.DEPLOY_HEROKU_PROJECT : self.deployHerokuProject,

            GitCommitter.ADD_ENVIRONMENT_VARIABLE : self.addEnvironmentVariable
        }

    def runCommandList(self,commandList):
        globals = self.globals
        returnSet = {}
        for projectName in self.projectNameList :
            try :
                returnSet[projectName] = {}
                processPath = f'{globals.localPath}{globals.apisRoot}{projectName}'
                for command in commandList :
                    # print(f'{globals.NEW_LINE}[{projectName}] {command}')
                    returnSet[projectName][command] = subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
                    # print(self.getProcessReturnValue(returnSet[projectName][command]))
                    # globals.debug(returnSet[projectName][command])
            except Exception as exception :
                print(f'{self.globals.ERROR}{projectName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')
        return returnSet

    def runCommandSet(self,commandSet,path=None):
        globals = self.globals
        returnSet = {}
        for projectName,commandList in commandSet.items() :
            try :
                returnSet[projectName] = {}
                for command in commandList :
                    if path :
                        processPath = path
                    else :
                        processPath = f'{globals.localPath}{globals.apisRoot}{projectName}'
                    # print(f'{globals.NEW_LINE}[{projectName}] {command} {processPath}')
                    returnSet[projectName][command] = subprocess.run(command,shell=True,capture_output=True,cwd=processPath)
                    # print(self.getProcessReturnValue(returnSet[projectName][command]))
            except Exception as exception :
                print(f'{self.globals.ERROR}{projectName}{globals.SPACE_DASH_SPACE}{command}{globals.NEW_LINE}{str(exception)}')
        return returnSet

    def setGlobalCredentials(self,commandList):
        userName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'User name',commandList)
        userEmail = self.getArg(GitCommitter._2_ARGUMENT_INDEX,f'User email',commandList)
        commandConfigGlobalUserName = GitCommand.CONFIG_GLOBAL_USER_NAME.replace(GitCommand.TOKEN_USER_NAME,userName)
        commandConfigGlobalUserEmail = GitCommand.CONFIG_GLOBAL_USER_EMAIL.replace(GitCommand.TOKEN_USER_EMAIL,userEmail)
        commandSet = {}
        for api in self.session.apiList :
            commandSet[api.projectName] = [
                commandConfigGlobalUserName,
                commandConfigGlobalUserEmail
            ]
        returnSet = self.runCommandSet(commandSet)
        return self.debugReturnSet('setGlobalCredentials',self.getReturnSetValue(returnSet))

    def deployHerokuProject(self,commandList):
        projectName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Project name',commandList)
        commitMessage = self.getArg(GitCommitter._2_ARGUMENT_INDEX,f'{projectName} commit message',commandList)
        if projectName :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            commandCheckoutMaster = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,GitCommand.KW_MASTER_BRANCH)
            commandMergeOriginDevelop = GitCommand.MERGE_ORIGIN.replace(GitCommand.TOKEN_BRANCH_NAME,GitCommand.KW_DEVELOP_BRANCH)
            returnSet = self.runCommandSet({projectName:[
                GitCommand.ADD,
                commandCommit,
                GitCommand.PUSH,
                GitCommand.PUSH,
                commandCheckoutMaster,
                commandMergeOriginDevelop,
                GitCommand.PUSH,
                GitCommand.PUSH_HEROKU_MASTER
            ]})
            return self.debugReturnSet('deployHerokuProject',self.getReturnSetValue(returnSet))

    def newReleaseAll(self,commandList):
        return GitCommitterNewRelease.newReleaseAll(self,commandList)

    def newReleaseProject(self,commandList):
        return GitCommitterNewRelease.newReleaseProject(self,commandList)

    def cloneProjectIfNeeded(self,commandList):
        globals = self.globals
        projectName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Project name',commandList)
        localProjectNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        commandSet = {}
        if not localProjectNameList or projectName not in localProjectNameList :
            projectUrl = f'{self.gitUrl}{projectName}.{self.gitExtension}'
            command = GitCommand.CLONE.replace(GitCommand.TOKEN_PROJECT_URL,projectUrl)
            processPath = f'{globals.localPath}{globals.apisRoot}'
            commandSet[projectName] = [command]
        else :
            print(f'{projectName} already exists')
        if commandSet :
            returnSet = {}
            returnSet = self.runCommandSet(commandSet,path=processPath)
            self.debugReturnSet('cloneProjectIfNeeded',self.getReturnSetValue(returnSet))
            return returnSet

    def addCommitPushProject(self,commandList):
        projectName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Project name',commandList)
        commitMessage = self.getArg(GitCommitter._2_ARGUMENT_INDEX,f'{projectName} commit message',commandList)
        if projectName :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandSet({projectName:[
                GitCommand.ADD,
                commandCommit,
                GitCommand.PUSH
            ]})
            self.debugReturnSet('addCommitPushProject',self.getReturnSetValue(returnSet))

    def cloneAllIfNeeded(self,commandList):
        globals = self.globals
        localProjectNameList = list(globals.getPathTreeFromPath(f'{globals.localPath}{globals.apisRoot}').keys())
        if localProjectNameList :
            commandSet = {}
            for api in self.session.apiList :
                if api.projectName not in localProjectNameList :
                    command = GitCommand.CLONE.replace(GitCommand.TOKEN_PROJECT_URL,api.gitUrl)
                    processPath = f'{globals.localPath}{globals.apisRoot}'
                    commandSet[api.projectName] = [command]
                else :
                    globals.warning(f'{api.projectName} already exists')
            if commandSet :
                returnSet = self.runCommandSet(commandSet,path=processPath)
                self.debugReturnSet('cloneAllIfNeeded',self.getReturnSetValue(returnSet))

    def checkoutBAllIfNeeded(self,commandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',commandList)
        if branchName :
            commandCheckoutAll = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandCheckoutAll])
            if returnSet and returnSet.items():
                for projectName,specificReturnSet in returnSet.items() :
                    if specificReturnSet and specificReturnSet.items() :
                        for key,value in specificReturnSet.items() :
                            if 'error' in self.getProcessReturnErrorValue(value) :
                                command = GitCommand.CHECKOUT_DASH_B.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
                                commandSet = {projectName:[command]}
                                returnCorrectionSet = self.runCommandSet(commandSet)
            self.debugReturnSet('checkoutBAllIfNeeded',self.getReturnSetValue(returnSet))

    def pushSetUpStreamOriginAllIfNedded(self,commandList):
        returnSet = self.runCommandList([GitCommand.PUSH])
        returnCorrectionSet = {}
        if returnSet and returnSet.items():
            for projectName,specificReturnSet in returnSet.items() :
                returnCorrectionSet[projectName] = {}
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        for line in self.getProcessReturnErrorValue(value).split(self.globals.NEW_LINE) :
                            if GitCommand.PUSH_SET_UPSTREAM_ORIGIN in line :
                                commandPush = GitCommand.BRANCH
                                returnCorrectionSet[projectName][commandPush] = self.runCommandSet({projectName:[commandPush]})[projectName][commandPush]
                                dirtyBranchNameList = self.getProcessReturnValue(returnCorrectionSet[projectName][commandPush]).split(self.globals.NEW_LINE)
                                if dirtyBranchNameList :
                                    for dirtyBranchName in dirtyBranchNameList :
                                        if '*' in dirtyBranchName :
                                            branchName = dirtyBranchName.split()[1].strip()
                                            commandPushSetUpStreamAll = GitCommand.PUSH_SET_UPSTREAM_ORIGIN_BRANCH.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
                                            returnCorrectionSet[projectName][commandPushSetUpStreamAll] = self.runCommandSet({projectName:[commandPushSetUpStreamAll]})[projectName][commandPushSetUpStreamAll]
        self.debugReturnSet('pushSetUpStreamOriginAllIfNedded',self.getReturnSetValue(returnSet))

    def addCommitPushSetUpStreamOriginAllIfNedded(self,commandList):
        print('Good luck implementing it')

    def statusAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.STATUS])
        self.debugReturnSet('statusAll',self.getReturnSetValue(returnSet))

    def branchAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.BRANCH])
        self.debugReturnSet('branchAll',self.getReturnSetValue(returnSet))

    def fetchAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.FETCH])
        self.debugReturnSet('fetchAll',self.getReturnSetValue(returnSet))

    def pullAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.PULL])
        self.debugReturnSet('pullAll',self.getReturnSetValue(returnSet))

    def checkoutAll(self,commandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',commandList)
        if branchName :
            commandCheckoutAll = GitCommand.CHECKOUT.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandCheckoutAll])
            self.debugReturnSet('checkoutAll',self.getReturnSetValue(returnSet))

    def addAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.ADD])
        self.debugReturnSet('addAll',self.getReturnSetValue(returnSet))

    def commitAll(self,commandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',commandList)
        if commitMessage :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandList([commandCommit])
            self.debugReturnSet('commitAll',self.getReturnSetValue(returnSet))

    def pushAll(self,commandList):
        returnSet = self.runCommandList([GitCommand.PUSH])
        self.debugReturnSet('pushAll',self.getReturnSetValue(returnSet))

    def addCommitPushAll(self,commandList):
        commitMessage = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Commit message',commandList)
        if commitMessage :
            commandCommit = GitCommand.COMMIT.replace(GitCommand.TOKEN_COMMIT_MESSAGE,commitMessage)
            returnSet = self.runCommandList([
                GitCommand.ADD,
                commandCommit,
                GitCommand.PUSH
            ])
            self.debugReturnSet('addCommitPushAll',self.getReturnSetValue(returnSet))

    def mergeOriginAll(self,commandList):
        branchName = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Branch name',commandList)
        if branchName :
            commandMergeOriginAll = GitCommand.MERGE_ORIGIN.replace(GitCommand.TOKEN_BRANCH_NAME,branchName)
            returnSet = self.runCommandList([commandMergeOriginAll])
            self.debugReturnSet('mergeOriginAll',self.getReturnSetValue(returnSet))

    def addEnvironmentVariable(self,commandList):
        variableKey = self.getArg(GitCommitter._1_ARGUMENT_INDEX,'Environment variable key',commandList)
        variableValue = self.getArg(GitCommitter._2_ARGUMENT_INDEX,'Environment variable value',commandList)
        if variableKey and variableValue :
            globals = self.globals
            if variableKey == GitCommand.KW_SELF :
                variableValue = f'{globals.localPath}{globals.apisRoot}{GitCommitter.__name__}{globals.BACK_SLASH}{globals.baseApiPath}'
                print(variableValue)
            os.environ[variableKey] = variableValue

    def wakeUpVoiceAssistant(self,commandList):
        self.voiceAssistant = VoiceAssistant.VoiceAssistant(self.globals)
        WakeUpVoiceAssistant.run(self)

    def getProcessReturnValue(self,processReturn):
        return str(processReturn.stdout,self.globals.ENCODING)

    def getProcessReturnErrorValue(self,processReturn):
        return str(processReturn.stderr,self.globals.ENCODING)

    def getReturnSetValue(self,returnSet):
        globals = self.globals
        returnValue = globals.NOTHING
        if returnSet and returnSet.items():
            for projectName,specificReturnSet in returnSet.items() :
                if specificReturnSet and specificReturnSet.items() :
                    for key,value in specificReturnSet.items() :
                        processReturnValue = self.getProcessReturnValue(value)
                        if processReturnValue and not globals.NOTHING == processReturnValue :
                            returnValue += f'{projectName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{processReturnValue}'
                        else :
                            returnValue += f'{projectName}{globals.SPACE_DASH_SPACE}{key}{globals.NEW_LINE}{self.getProcessReturnErrorValue(value)}'
                    returnValue += globals.NEW_LINE
        return returnValue

    def printReturn(self,processReturn):
        print(self.getReturnValue(processReturn))

    def debugReturnSet(self,callMethodName,ReturnSetValue):
        self.globals.debug(f'{callMethodName}{2 * self.globals.NEW_LINE}{ReturnSetValue}')

    def getArg(self,argIndex,typingGetMessage,commandList) :
        try :
            if '()' in commandList[argIndex] :
                return self.validInput(self.getImput(typingGetMessage))
            return commandList[argIndex]
        except Exception as exception :
            self.globals.debug(f'Not possible to get commandList[{argIndex}]. Cause: {str(exception)}')
            return self.validInput(self.getImput(typingGetMessage))

    def validInput(self,input):
        if input == GitCommitter.SKIP :
            return None
        else :
            return input

    def getImput(self,typingGetMessage):
        return input(f'{typingGetMessage}{Constant.COLON_SPACE}')

    def getProjectNameList(self):
        if self.session :
            projectNameList = []
            for api in self.session.apiList :
                projectNameList.append(api.projectName)
            return projectNameList
        else :
            return self.globals.apiNameList
