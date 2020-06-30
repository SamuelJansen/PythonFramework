import sqlalchemy
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UnicodeText, MetaData, Sequence, DateTime

UnicodeText = UnicodeText
DateTime = DateTime

Table = Table
Column = Column
Integer = Integer
String = String

exists = exists

relationship = relationship

Sequence = Sequence
ForeignKey = ForeignKey
MetaData = MetaData

KW_API = 'api'
KW_NAME = 'name'
KW_MAIN_URL = 'main-url'

KW_REPOSITORY = 'repository'
KW_REPOSITORY_DIALECT = 'dialect'
KW_REPOSITORY_USER = 'user'
KW_REPOSITORY_PASSWORD = 'password'
KW_REPOSITORY_HOST = 'host'
KW_REPOSITORY_PORT = 'port'
KW_REPOSITORY_DATABASE = 'database'

def getNewModel() :
    return declarative_base()

class SqlAlchemyHelper:

    TOKEN_WITHOUT_NAME = '__TOKEN_WITHOUT_NAME__'

    DEFAULT_DATABASE_TYPE = 'sqlite'
    BAR = '''/'''
    COLON = ''':'''
    ARROBA = '''@'''
    DOUBLE_BAR = 2 * BAR
    TRIPLE_BAR = 3 * BAR

    NOTHING = ''

    EXTENSION = 'db'

    def __init__(self,
            name = TOKEN_WITHOUT_NAME,
            dialect = None,
            user = None,
            password = None,
            host = None,
            port = None,
            model = None,
            globals = None,
            echo = False
        ):

        self.sqlalchemy = sqlalchemy

        if not dialect and globals :
            self.dialect = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DIALECT}')
        else :
            self.dialect = dialect

        if not dialect and globals :
            self.user = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_USER}')
        else :
            self.user = user

        if not dialect and globals :
            self.password = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PASSWORD}')
        else :
            self.password = password

        if not dialect and globals :
            self.host = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_HOST}')
        else :
            self.host = host

        if not dialect and globals :
            self.port = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_PORT}')
        else :
            self.port = port

        if name == self.TOKEN_WITHOUT_NAME and globals :
            self.name = globals.getApiSetting(f'{KW_API}.{KW_REPOSITORY}.{KW_REPOSITORY_DATABASE}')
        else :
            self.name = name

        if globals :
            globals.debug(f'Repository consiguration:')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}dialect = {self.dialect}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}user = wops!')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}password = wops!')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}host = {self.host}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}port = {self.port}')
            globals.debug(f'{globals.TAB_UNITS * globals.SPACE}name = {self.name}')

        user_password_host = self.NOTHING
        if self.user and self.password :
            user_password_host += f'{self.user}{self.COLON}{self.password}'
        if self.host :
            user_password_host += f'{self.ARROBA}{self.host}{self.COLON}{self.port}'
        user_password_host += self.BAR

        if user_password_host == self.BAR :
            self.name = f'{self.name}.{self.EXTENSION}'

        if not self.dialect :
            self.dialect = self.DEFAULT_DATABASE_TYPE

        self.databaseUrl = f'{self.dialect}:{self.DOUBLE_BAR}{user_password_host}{self.name}'

        self.engine = create_engine(self.databaseUrl, echo=echo)
        self.session = scoped_session(sessionmaker(self.engine)) ###- sessionmaker(bind=self.engine)()
        self.model = model
        self.model.metadata.bind = self.engine
        self.run()

    def run(self):
        self.model.metadata.create_all(self.engine)

    def saveNewAndCommit(self,*args):
        model = args[-1]
        return self.saveAndCommit(model(*args[:-1]))

    def saveAndCommit(self,instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    def saveAllAndCommit(self,instanceList):
        self.session.add_all(instanceList)
        self.session.commit()
        return instanceList

    def findAllAndCommit(self,model):
        objectList = self.session.query(model).all()
        self.session.commit()
        return objectList

    def findByIdAndCommit(self,id,model):
        object = self.session.query(model).filter(model.id == id).first()
        self.session.commit()
        return object

    def existsByIdAndCommit(self,id,model):
        # ret = Session.query(exists().where(and_(Someobject.field1 == value1, Someobject.field2 == value2)))
        objectExists = self.session.query(exists().where(model.id == id)).one()[0]
        self.session.commit()
        return objectExists

    def findByKeyAndCommit(self,key,model):
        object = self.session.query(model).filter(model.key == key).first()
        self.session.commit()
        return object

    def existsByKeyAndCommit(self,key,model):
        objectExists = self.session.query(exists().where(model.key == key)).one()[0]
        self.session.commit()
        return objectExists

    def findByStatusAndCommit(self,status,model):
        object = self.session.query(model).filter(model.status == status).first()
        self.session.commit()
        return object

    def findAllByQueryAndCommit(self,query,model):
        if query :
            objectList = self.session.query(model).filter_by(**query).all()
            self.session.commit()
            return objectList
        return []
