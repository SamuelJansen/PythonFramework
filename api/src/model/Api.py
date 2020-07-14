from SqlAlchemyHelper import *
from FrameworkModel import *
from Session import *
from python_helper import Constant

class Api(Model):
    __tablename__ = API

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    projectName = Column(String(128),unique=True)
    className = Column(String(128),unique=True)
    gitUrl = Column(String(256),unique=True)

    importScript = Column(String(1024),unique=True)
    sessionList = relationship(SESSION, secondary=apiToSessionAssociation, back_populates=f'{attributeIt(__tablename__)}{LIST}')

    def __init__(self,key,projectName,className,gitUrl,importScript,sessionList):
        self.key = key
        self.projectName = projectName
        self.className = className
        self.gitUrl = gitUrl
        self.importScript = importScript
        self.sessionList = sessionList

        self.strImportScript = f', importScript={Constant.SPACE.join(self.importScript.replace(Constant.NEW_LINE,Constant.NOTHING).split())}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, key={self.key}, projectName={self.projectName}, className={self.className})'
