class GitCommand:

    API_KEY_GIT_COMMITTER = 'git-committer'

    KW_GIT = 'git'
    KW_SELF = 'self'
    KW_CLONE = 'clone'
    KW_STATUS = 'status'
    KW_BRANCH = 'branch'
    KW_PULL = 'pull'
    KW_CHECKOUT = 'checkout'
    KW_ADD = 'add'
    KW_COMMIT = 'commit'
    KW_PUSH = 'push'
    KW_FETCH = 'fetch'
    KW_MERGE = 'merge'
    KW_ORIGIN = 'origin'
    KW_SET_UPSTREAM = 'set-upstream'

    KW_CONFIG = 'config'
    KW_GLOBAL = 'global'
    KW_USER = 'user'
    KW_NAME = 'name'
    KW_EMAIL = 'email'

    KW_MASTER_BRANCH = 'master' ###- deprecated. Use api.mainBranch insted
    KW_DEVELOP_BRANCH = 'develop'


    TOKEN_USER_NAME = '__TOKEN_USER_NAME__'
    TOKEN_USER_EMAIL = '__TOKEN_USER_EMAIL__'

    TOKEN_PROJECT_URL = '__TOKEN_PROJECT_URL__'
    TOKEN_COMMIT_MESSAGE = '__TOKEN_COMMIT_MESSAGE__'
    TOKEN_BRANCH_NAME = '__TOKEN_BRANCH_NAME__'

    TOKEN_RELEASE_VERSION = '__TOKEN_RELEASE_VERSION__'
    TOKEN_TARGET = '__TOKEN_TARGET__'
    TOKEN_TITLE = '__TOKEN_TITLE__'
    TOKEN_DESCRIPTION = '__TOKEN_DESCRIPTION__'


    CONFIG_GLOBAL_USER_NAME = f'{KW_GIT} {KW_CONFIG} --{KW_GLOBAL} {KW_USER}.{KW_NAME} "{TOKEN_USER_NAME}"'
    CONFIG_GLOBAL_USER_EMAIL = f'{KW_GIT} {KW_CONFIG} --{KW_GLOBAL} {KW_USER}.{KW_EMAIL} "{TOKEN_USER_EMAIL}"'

    CLONE = f'{KW_GIT} {KW_CLONE} {TOKEN_PROJECT_URL}'
    STATUS = f'{KW_GIT} {KW_STATUS}'
    BRANCH = f'{KW_GIT} {KW_BRANCH}'
    PULL = f'{KW_GIT} {KW_PULL}'
    CHECKOUT = f'{KW_GIT} {KW_CHECKOUT} {TOKEN_BRANCH_NAME}'
    CHECKOUT_DASH_B = f'{KW_GIT} {KW_CHECKOUT} -b {TOKEN_BRANCH_NAME}'
    ADD = f'{KW_GIT} {KW_ADD} .'
    COMMIT = f'{KW_GIT} {KW_COMMIT} -m "{TOKEN_COMMIT_MESSAGE}"'
    PUSH = f'{KW_GIT} {KW_PUSH}'
    FETCH = f'{KW_GIT} {KW_FETCH}'
    MERGE = f'{KW_GIT} {KW_MERGE}'
    ORIGIN = f'{KW_GIT} {KW_ORIGIN}'
    MERGE_ORIGIN = f'{KW_GIT} {KW_MERGE} {KW_ORIGIN}/{TOKEN_BRANCH_NAME}'
    PUSH_SET_UPSTREAM_ORIGIN = f'{KW_GIT} {KW_PUSH} --set-upstream {KW_ORIGIN}'
    PUSH_SET_UPSTREAM_ORIGIN_BRANCH = f'{PUSH_SET_UPSTREAM_ORIGIN} {TOKEN_BRANCH_NAME}'

    NEW_RELEASE = f'{TOKEN_PROJECT_URL}/releases/new?tag=v{TOKEN_RELEASE_VERSION}&target={TOKEN_TARGET}&title={TOKEN_TITLE}&body={TOKEN_DESCRIPTION}'

    PUSH_HEROKU_MASTER = f'{KW_GIT} {KW_PUSH} heroku {TOKEN_BRANCH_NAME}'
