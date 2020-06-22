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

# Model = declarative_base()

def getNewModel() :
    return declarative_base()

class SqlAlchemyHelper:

    DEFAULT_DATABASE_TYPE = 'sqlite'
    BAR = '''/'''
    COLON = ''':'''
    ARROBA = '''@'''
    DOUBLE_BAR = 2 * BAR
    TRIPLE_BAR = 3 * BAR

    NOTHING = ''

    EXTENSION = 'db'

    def __init__(self,name,
            dialect = DEFAULT_DATABASE_TYPE,
            user = None,
            password = None,
            host = None,
            port = None,
            model = None,
            echo = False):
        self.sqlalchemy = sqlalchemy
        self.name = name
        self.dialect = dialect
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        use_password_host = self.NOTHING
        if self.user and self.password :
            use_password_host += f'{self.user}{self.COLON}{self.password}'
        if self.host :
            use_password_host += f'{self.ARROBA}{self.host}{self.COLON}{self.port}'
        use_password_host += self.BAR

        if use_password_host == self.BAR :
            self.name = f'{self.name}.{self.EXTENSION}'

        if not self.dialect :
            self.dialect = self.DEFAULT_DATABASE_TYPE

        self.databaseUrl = f'{self.dialect}:{self.DOUBLE_BAR}{use_password_host}{self.name}'
        print(f'self.databaseUrl = {self.databaseUrl}')

        self.engine = create_engine(self.databaseUrl, echo=echo)
        self.session = scoped_session(sessionmaker(self.engine)) ###- sessionmaker(bind=self.engine)()
        self.model = model
        self.model.metadata.bind = self.engine
        self.run()

    def run(self):
        self.model.metadata.create_all(self.engine)

    def saveNew(self,*args):
        model = args[-1]
        return self.save(model(*args[:-1]))

    def save(self,instance):
        self.session.add(instance)
        self.session.commit()
        return instance

    def saveAll(self,instanceList):
        self.session.add_all(instanceList)
        self.session.commit()
        return instanceList

    def findAll(self,model):
        return self.session.query(model).all()

    def findById(self,id,model):
        return self.session.query(model).filter(model.id == id).first()

    def existsById(self,id,model):
        # ret = Session.query(exists().where(and_(Someobject.field1 == value1, Someobject.field2 == value2)))
        return self.session.query(exists().where(model.id == id)).one()[0]

    def findByKey(self,key,model):
        return self.session.query(model).filter(model.key == key).first()

    def existsByKey(self,key,model):
        return self.session.query(exists().where(model.key == key)).one()[0]

    def findByStatus(self,status,model):
        return self.session.query(model).filter(model.status == status).first()

    def findAllByQuery(self,query,model):
        if query :
            return self.session.query(model).filter_by(**query).all()
        return []
