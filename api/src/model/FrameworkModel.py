from SqlAlchemyProxy import *

Model = getNewModel()

API = 'Api'
SESSION = 'Session'
apiList, sessionList, manySisterToManyBrother = getManyToMany(API, SESSION, Model)
