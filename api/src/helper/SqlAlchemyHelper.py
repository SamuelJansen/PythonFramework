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

DATABASE_LAST_NAME = '-database'

def getNewModel() :
    return declarative_base()

class SqlAlchemyHelper:

    DEFAULT_DATABASE_TYPE = 'sqlite'
    TRIPLE_BAR = '///'
    EXTENSION = 'db'

    def __init__(self,firstName,type=DEFAULT_DATABASE_TYPE,model=None,extension=EXTENSION,echo=False):
        self.sqlalchemy = sqlalchemy
        self.firstName = firstName
        self.type = type
        self.extension = extension
        self.engine = create_engine(f'{self.type}:{self.TRIPLE_BAR}{self.firstName}{DATABASE_LAST_NAME}.{self.extension}', echo=echo)
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
