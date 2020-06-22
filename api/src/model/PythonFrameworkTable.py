from SqlAlchemyHelper import *

CLASS_API = 'Api'
CLASS_SESSION = 'Session'

API = CLASS_API.lower()
SESSION = CLASS_SESSION.lower()
Model = getNewModel()

def getManyToMany(son, father):
    return Table(f'{son}_to_{father}', Model.metadata,
        Column(f'{son}_id', Integer, ForeignKey(f'{son}.id')),
        Column(f'{father}_id', Integer, ForeignKey(f'{father}.id')))
