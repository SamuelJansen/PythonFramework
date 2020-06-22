from SqlAlchemyHelper import *
from TableName import *

apiToSessionAssociation = getManyToMany(API, SESSION)

class Session(Model):
    __tablename__ = SESSION

    id = Column(Integer(), Sequence(f'{__tablename__}_id_seq'), primary_key=True)
    key = Column(String(128),unique=True)
    status = Column(String(64),unique=True)
    api_list = relationship(CLASS_API, secondary=apiToSessionAssociation, back_populates=f'{__tablename__}_list')

    def __init__(self,key,status,api_list):
        self.key = key
        self.status = status
        self.api_list = api_list

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, key={self.key}, status={self.status}, api_list={self.api_list})'
