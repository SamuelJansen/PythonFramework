from SqlAlchemyProxy import *
from python_helper import Constant
import FrameworkModel

API = FrameworkModel.API
SESSION = FrameworkModel.SESSION

class Api(FrameworkModel.Model):
    __tablename__ = API

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128),unique=True)
    projectName = Column(String(128),unique=True)
    className = Column(String(128),unique=True)
    gitUrl = Column(String(256),unique=True)
    mainBranch = Column(String(16),default='main')

    importScript = Column(String(1024),unique=True)
    sessionList = FrameworkModel.sessionList ###- relationship(SESSION, secondary=FrameworkModel.apiToSessionAssociation, back_populates=f'{attributeIt(__tablename__)}{LIST}')
    # sessionList = getRightSideManyToMany(API, SESSION, FrameworkModel.Model)

    def __init__(self,key,projectName,className,gitUrl,importScript,sessionList,mainBranch='main'):
        self.key = key
        self.projectName = projectName
        self.className = className
        self.gitUrl = gitUrl
        self.importScript = importScript
        self.sessionList = sessionList
        self.mainBranch = mainBranch

        self.strImportScript = f', importScript={Constant.SPACE.join(self.importScript.replace(Constant.NEW_LINE,Constant.NOTHING).split())}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, key={self.key}, projectName={self.projectName}, className={self.className})'
