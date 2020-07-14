from SqlAlchemyHelper import *
import FrameworkModel

API = FrameworkModel.API
SESSION = FrameworkModel.SESSION

class Session(FrameworkModel.Model):
    __tablename__ = SESSION

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    key = Column(String(128), unique=True)
    status = Column(String(64))
    apiList = relationship(API, secondary=FrameworkModel.apiToSessionAssociation, back_populates=f'{attributeIt(__tablename__)}{LIST}')

    def __init__(self,key,status,apiList):
        self.key = key
        self.status = status
        self.apiList = apiList

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, key={self.key}, status={self.status}, apiList={self.apiList})'
