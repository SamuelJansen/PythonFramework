from SqlAlchemyHelper import *

class Api(Model):
    __tablename__ = 'api'

    id = Column(Integer(), Sequence(f'{__tablename__}_id_seq'), primary_key=True)
    key = Column(String(128),unique=True)
    className = Column(String(128),unique=True)
    gitUrl = Column(String(256),unique=True)
    importScript = Column(String(1024),unique=True)

    def __init__(self,key,className,gitUrl,importScript):
        self.key = key
        self.className = className
        self.gitUrl = gitUrl
        self.importScript = importScript

    def __repr__(self):
        return f'id = {self.id}\nkey = {self.key}\nclassName = {self.className}\ngitUrl = {self.gitUrl}\nimportScript = {self.importScript}'
