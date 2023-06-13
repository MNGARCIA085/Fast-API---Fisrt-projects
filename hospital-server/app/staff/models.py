from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship,backref
from database.configuration import Base
from auth.models import User



class Especialidad(Base):
    __tablename__ = 'especialidad'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String)
    doctor = relationship('Doctor', secondary='doctor_especialidades')



# Test table
class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer,primary_key=True)
    descripcion = Column(String)
    test = Column(String)


# carga horaria
class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True)
    # fk de test
    child_id = Column(Integer, ForeignKey('child.id'))
    child = relationship("Child", backref=backref("doctor", uselist=False, cascade="all,delete"))
    # FK A user
    #user = Column(Integer, ForeignKey('user.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref=backref("doctor", uselist=False))
    especialidad = relationship('Especialidad', secondary='doctor_especialidades')




class DoctorEspecialidades(Base):
    __tablename__ = 'doctor_especialidades'
    doctor_id = Column(Integer, ForeignKey('doctor.id'), primary_key=True)
    especialidad_id = Column(Integer, ForeignKey('especialidad.id'), primary_key=True)