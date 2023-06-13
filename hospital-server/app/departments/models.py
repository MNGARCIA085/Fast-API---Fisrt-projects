from sqlalchemy import Column, Integer, String
from database.configuration import Base


class Sede(Base):
   __tablename__= "sede"
   
   id=Column(Integer, primary_key= True) 
   tipo = Column(String) # clinica, poli
   direccion = Column(String)
   nombre = Column(String)
   # tels.
   
   






"""

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Exercise(Base):
   __tablename__= "Exercise"
   id=Column(Integer, primary_key= True) 
   name=Column(VARCHAR(250))
   animation_id=Column(Integer, ForeignKey('Animation.id')) #foreign key -> animation.id
   animation=relationship("Animation", back_populates="exercise")
   

class Animation(Base):
   __tablename__="Animation"
   id=Column(Integer,primary_key=True,index=True,autoincrement=True)
   name=Column(VARCHAR(250))
   description=Column(VARCHAR(250))
   exercise=relationship("Exercise", back_populates="animation")
"""