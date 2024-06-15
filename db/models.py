from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base
import datetime
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
	
class Meet(Base):
    __tablename__ = "meets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    persons_ids:list[int] = Column(ARRAY(Integer), default=[])
    names:dict[str,int] = Column(JSON(), default={})
    datetime = Column(DateTime, default=datetime.datetime.now)
    watched = Column(Boolean, default=False)
    photo = Column(String, nullable=True)
    
class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    image_path = Column(String)
    used = Column(Boolean, default=False)