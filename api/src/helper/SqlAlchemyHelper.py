import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, UnicodeText, MetaData, Sequence, DateTime

UnicodeText = UnicodeText
DateTime = DateTime

Table = Table
Column = Column
Integer = Integer
String = String

relationship = relationship

Sequence = Sequence
ForeignKey = ForeignKey
MetaData = MetaData

Model = declarative_base()

DATABASE_LAST_NAME = '-database'

class SqlAlchemyHelper:

    DEFAULT_DATABASE_TYPE = 'sqlite'
    TRIPLE_BAR = '///'
    EXTENSION = 'db'

    def __init__(self,firstName,type=DEFAULT_DATABASE_TYPE,extension=EXTENSION,echo=False):
        self.sqlalchemy = sqlalchemy
        self.firstName = firstName
        self.type = type
        self.extension = extension
        self.engine = create_engine(f'{self.type}:{self.TRIPLE_BAR}{self.firstName}{DATABASE_LAST_NAME}.{self.extension}', echo=echo)
        self.session = scoped_session(sessionmaker(self.engine)) ###- sessionmaker(bind=self.engine)()
        self.Model = Model
        self.Model.metadata.bind = self.engine

    def run(self):
        Model.metadata.create_all(self.engine)

    def save(self,instance):
        self.session.add(instance)
        self.session.commit()

    def saveAll(self,instanceList):
        self.session.add_all(instanceList)
        self.session.commit()

    def findAll(self,model):
        return self.session.query(model).all()

    def findById(self,model,id):
        return self.session.query(model).filter(model.id == id).first()

    def findByKey(self,model,key):
        return self.session.query(model).filter(model.key == key).first()
