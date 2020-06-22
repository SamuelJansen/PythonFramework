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

    TOKEN_PROJECT_URL = '__TOKEN_PROJECT_URL__'
    TOKEN_COMMIT_MESSAGE = '__TOKEN_COMMIT_MESSAGE__'
    TOKEN_BRANCH_NAME = '__TOKEN_BRANCH_NAME__'

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