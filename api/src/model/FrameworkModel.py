from SqlAlchemyHelper import *

Model = getNewModel()

API = 'Api'
SESSION = 'Session'
apiToSessionAssociation = getManyToMany(API, SESSION, Model)
