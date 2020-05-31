from SqlAlchemyHelper import *
from TableName import *
from Session import *

class Api(Model):
    __tablename__ = API

    id = Column(Integer(), Sequence(f'{__tablename__}_id_seq'), primary_key=True)
    key = Column(String(128),unique=True)
    class_name = Column(String(128),unique=True)
    git_url = Column(String(256),unique=True)
    import_script = Column(String(1024),unique=True)
    session_list = relationship(CLASS_SESSION, secondary=apiToSessionAssociation, back_populates=f'{__tablename__}_list')

    def __init__(self,key,class_name,git_url,import_script,session_list):
        self.key = key
        self.class_name = class_name
        self.git_url = git_url
        self.import_script = import_script
        self.session_list = session_list

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, key={self.key}, class_name={self.class_name}, git_url={self.git_url}, import_script={self.import_script})'
